from heapq import merge
import math
import os
import time
import sys

#Uncomment this if the script will run within AEDT with Ironpython. Setup the path where pyaedt folder is.
#path_to_pyaedt_root_folder=""
#sys.path.append(path_to_pyaedt_root_folder)


from pyaedt import Edb, Hfss3dLayout, is_ironpython
from pyaedt.generic.general_methods import number_aware_string_key
from pyaedt.generic.toolkit import WPFToolkit, launch, select_directory
import json



class ApplicationWindow(WPFToolkit):

    def __init__(self):
        WPFToolkit.__init__(self, toolkit_file=__file__, aedt_design=None, parent_design_name=None)
        # Copy Xaml template
        json_path = os.path.join(os.path.dirname(__file__), "merge_wizard_settings.json")
        if os.path.exists(json_path):
            with open(json_path) as f:
                config = json.load(f)
            desktop_version = config.get("desktop_version", "2021.2")
            host = config.get("host", "")
            if host and not os.path.exists(os.path.join(os.path.dirname(__file__), host)):
                host = os.path.join(os.path.dirname(__file__), host)
            merge = config.get("merge", "")
            if merge and not os.path.exists(os.path.join(os.path.dirname(__file__), host)):
                merge = os.path.join(os.path.dirname(__file__), merge)
            self.load_layout_on_init = config.get("load_layout_on_init", "0") == "1"
            self.host_component = config.get("host_component", None)
            self.merge_component = config.get("merge_component", None)
            self.design_1_pin1 = config.get("design_1_pin1", None)
            self.design_1_pin2 = config.get("design_1_pin2", None)
            self.design_2_pin1 = config.get("design_2_pin1", None)
            self.design_2_pin2 = config.get("design_2_pin2", None)
            self.enable_automatic_placement = config.get("enable_automatic_placement", "0") == "1"
            xoffset = config.get("xoffset", "0.0")
            yoffset = config.get("yoffset", "0.0")
            zoffset = config.get("zoffset", "0.0")
            rotation = config.get("rotation", "0")
            flip_layout = config.get("flip_layout", "0") == "1"
            flip_host_layout = config.get("flip_host_layout", "0") == "1"
            open_3d_layout = config.get("open_3d_layout", "0") == "1"
            placement_3d = config.get("placement_3d", "0") == "1"
            self.evaluate_placement_on_init = config.get("evaluate_placement_on_init", "0") == "1"
            self.execute_merge_on_init = config.get("execute_merge_on_init", "0") == "1"
        else:
            desktop_version= "2021.2"
            host = r'C:\Temp\package_on_board\board.aedb'
            merge = r'C:\Temp\package_on_board\package.aedb'
            self.load_layout_on_init = False
            self.host_component = None
            self.merge_component = None
            self.design_1_pin1 = None
            self.design_1_pin2 = None
            self.design_2_pin1 = None
            self.design_2_pin2 = None
            xoffset = "0.0"
            yoffset = "0.0"
            zoffset = "0.0"
            rotation = "0"
            flip_layout = True
            flip_host_layout = True
            open_3d_layout = False
            placement_3d = False
            self.host_edb_top_layer = ""
            self.host_edb_bottom_layer = ""
            self.source_edb_top_layer = ""
            self.source_edb_bottom_layer = ""
            self.evaluate_placement_on_init = False
            self.execute_merge_on_init = False
            self.enable_automatic_placement = True
        self.copy_xaml_template()
        self.edit_window_size(900, 400, "Pyaedt EDB Merge Utility")
        #Edit the UI

        self.add_label("label1", "Source Layout", 10, 50)
        self.add_text_box(name="merged", x_pos=150, y_pos=50, width=600, callback_method=self.load_source_design)
        self.add_button("merged_path_button", "Browse...", x_pos=760,  y_pos=50, callback_method=self.browse_design1)

        self.add_label("label2", "Host Layout", 10, 90)
        self.add_text_box(name="host", x_pos=150, y_pos=90, width=600, callback_method=self.load_host_design)
        self.add_button("host_path_button", "Browse...", x_pos=760,  y_pos=90, callback_method=self.browse_design2)

        self.add_label("label7", "Desktop Version", 10, 10)
        self.add_text_box(name="desktop_version", x_pos=150, y_pos=10, callback_method=self.validate_string_no_spaces,
                          callback_action='LostFocus')
        #self.add_check_box("placement_3d", "3d Placement", x_pos=300, y_pos=10)


        y_pos = 165
        self.add_label("label_host_layer", "Host design layer", 150, 110)
        self.add_combo_box("host_design_layers", x_pos=150, y_pos=130)
        self.add_label("label_source_layer", "Source design layer", 275, 110)
        self.add_combo_box("source_design_layers", x_pos=275, y_pos=130)
        #self.add_check_box("place_on_top_check", "Flip host layout", x_pos=150, y_pos=125)
        #self.add_check_box("flip_check", "Flip source layout", x_pos=275, y_pos=125)
        self.add_check_box("open_layout", "Open 3D Layout after merge", x_pos=400, y_pos=130)

        if self.enable_automatic_placement:
            # self.add_button("load_layout_button", "Load project", x_pos=600, y_pos=120, callback_method=self.load_layout)
            self.add_button("evaluate_vector_button", "Evaluate placement", x_pos=750, y_pos=120,
                            callback_method=self.evaluate_component_placement)

            self.add_label("label36", "Merged Component", 10, 165)
            self.add_combo_box("combo_box_merged_cmp", x_pos=150, y_pos=165, callback_action='SelectionChanged',
                               callback_method=self.update_merged_cmp)
            self.add_label("label17", "Host Component", 10, 205)
            self.add_combo_box("combo_box_host_cmp", x_pos=150, y_pos=205, callback_action='SelectionChanged',
                               callback_method=self.update_host_cmp)
            self.add_label("label_pin_matching", "Pin matching", 300, 165)
            self.add_label("label_pin_matching2", "Pin matching", 300, 205)
            self.add_combo_box("merged_pin1", x_pos=400, y_pos=165)
            self.add_combo_box("merged_pin2", x_pos=550, y_pos=165)

            self.add_combo_box("host_pin1", x_pos=400, y_pos=205)
            self.add_combo_box("host_pin2", x_pos=550, y_pos=205)
            y_pos = 250
        self.merged_edb = None
        self.host_edb = None
        mod = sys.modules["__main__"]
        if "oDesktop" in dir(mod):
            desktop_version = mod.oDesktop.GetVersion()[0:6]

        self.add_label("label4", "Rotation (deg)", 10, y_pos)
        self.add_text_box(name="rotation", x_pos=100, y_pos=y_pos, width=75, callback_method=self.validate_float,
                          callback_action='LostFocus')

        self.add_label("label5", "X Offset (mm)", 200, y_pos)
        self.add_text_box(name="xoffset", x_pos=300, y_pos=y_pos, width=75, callback_method=self.validate_float,
                          callback_action='LostFocus')

        self.add_label("label6", "Y Offset (mm)", 400, y_pos)
        self.add_text_box(name="yoffset", x_pos=500, y_pos=y_pos, width=75, callback_method=self.validate_float,
                          callback_action='LostFocus')

        self.add_label("label3", "Solder height (read-only, um)", 575, y_pos)
        self.add_text_box(name="zoffset", x_pos=750, y_pos=y_pos, width=75)

        y_pos += 50
        self.add_button("execute_button", "Merge layouts", x_pos=350, y_pos=y_pos, callback_method=self.launch_merge)
        self.launch_gui()
        self.set_text_value("desktop_version", desktop_version)
        self.set_text_value("merged", merge)
        self.set_text_value("host", host)
        self.set_text_value("rotation", rotation)
        self.set_text_value("xoffset", xoffset)
        self.set_text_value("yoffset", yoffset)
        self.set_text_value("zoffset", zoffset)
        solder_height_box = self.get_ui_object("zoffset")
        solder_height_box.IsEnabled = False
        #self.set_chechbox_status("place_on_top_check", flip_host_layout)
        #self.set_chechbox_status("placement_3d", placement_3d )
        #self.set_chechbox_status("flip_check", flip_layout)
        self.set_chechbox_status("open_layout", open_3d_layout)
        if self.load_layout_on_init:
            self.load_layout(None, None)
            if self.evaluate_placement_on_init:
                self.evaluate_component_placement(None, None)
            if self.execute_merge_on_init:
                self.launch_merge(None, None)

    @property
    def is_source_project_loaded(self):
        return self.merged_edb is not None and not self.merged_edb.db.IsNull()

    @property
    def is_host_project_loaded(self):
        return self.host_edb is not None and not self.host_edb.db.IsNull()

    @property
    def are_projects_loaded(self):
        return self.is_host_project_loaded and self.is_source_project_loaded

    def load_layout(self, sender, e):
        self.load_source_design(sender, e)
        self.load_host_design(sender, e)

    def unload_source_design(self):
        if self.merged_edb is not None:
            print("Closing source design")
            self.merged_edb.close_edb()
        self.clear_combobox_items("source_design_layers")
        self.clear_combobox_items("combo_box_merged_cmp")

    def load_source_design(self, sender, e):
        aedb_folder = self.ui.text_value("merged")
        if not os.path.isdir(aedb_folder):
            self.message_box("Source design path must be a directory")
            self.unload_source_design()
            return
        if self.is_source_project_loaded:
            if os.path.abspath(aedb_folder) == os.path.abspath(self.merged_edb.edbpath):
                return
            else:
                self.unload_source_design()

        desktop_version = self.get_text_value("desktop_version")
        self.merged_edb = Edb(edbpath=aedb_folder, edbversion=desktop_version)
        if self.merged_edb.db.IsNull():
            self.message_box("Failed to load design {}".format(aedb_folder), icon="Error")
            return

        merged_edb_layers = [str(i) for i in self.merged_edb.core_stackup.signal_layers.keys()]
        self.source_edb_top_layer, self.source_edb_bottom_layer = merged_edb_layers[-1], merged_edb_layers[0]
        self.add_combo_items("source_design_layers", [self.source_edb_top_layer, self.source_edb_bottom_layer],
            default=self.source_edb_bottom_layer)

        component_names = [str(i) for i in self.merged_edb.core_components.components.keys()]
        component_names.sort(key=number_aware_string_key)
        self.add_combo_items("combo_box_merged_cmp", component_names, default=self.merge_component)

        self.message_box("Loaded source design {}".format(aedb_folder))
        return

    def unload_host_design(self):
        if self.host_edb is not None:
            print("Closing host design")
            self.host_edb.close_edb()
        self.clear_combobox_items("host_design_layers")
        self.clear_combobox_items("combo_box_host_cmp")

    def load_host_design(self, sender, e):
        aedb_folder = self.ui.text_value("host")
        if not os.path.isdir(aedb_folder):
            self.message_box("Host design path must be a directory")
            self.unload_host_design()
            return
        if self.is_host_project_loaded:
            if os.path.abspath(aedb_folder) == os.path.abspath(self.host_edb.edbpath):
                return
            else:
                self.unload_host_design()

        desktop_version = self.get_text_value("desktop_version")
        self.host_edb = Edb(edbpath=aedb_folder, edbversion=desktop_version)
        if self.host_edb.db.IsNull():
            self.message_box("Failed to load design {}".format(aedb_folder), icon="Error")
            return

        host_edb_layers = [str(i) for i in self.host_edb.core_stackup.signal_layers.keys()]
        self.host_edb_top_layer, self.host_edb_bottom_layer = host_edb_layers[-1], host_edb_layers[0]
        self.add_combo_items("host_design_layers", [self.host_edb_top_layer, self.host_edb_bottom_layer],
            default=self.host_edb_top_layer)

        component_names = [str(i) for i in self.host_edb.core_components.components.keys()]
        component_names.sort(key=number_aware_string_key)
        self.add_combo_items("combo_box_host_cmp", component_names, default=self.host_component)

        self.message_box("Loaded host design {}".format(aedb_folder))
        return

    def browse_design1(self, sender, e):
        aedb_folder = select_directory(description="Merged Aedb Path")
        self.set_text_value("merged", aedb_folder)
        self.load_source_design(sender, e)

    def browse_design2(self, sender, e):
        aedb_folder = select_directory(description="Host Aedb Path")
        self.set_text_value("host", aedb_folder)
        self.load_host_design(sender, e)

    def enable_checkbox(self, sender, e):
        print("Enabled")

    def disable_checkbox(self, sender, e):
        print("Disabled")

    def aedt_add_log(self, text):
        self.aedtdesign.logger.info(text)

    def update_merged_cmp(self, sender, e):
        self.clear_combobox_items("merged_pin1")
        self.clear_combobox_items("merged_pin2")
        if not self.is_source_project_loaded:
            return

        cmp_pins = [str(pin.GetName())
                    for pin in self.merged_edb.core_components.get_pin_from_component(sender.SelectedItem)]
        cmp_pins.sort(key=number_aware_string_key)
        self.add_combo_items("merged_pin1", cmp_pins, default=self.design_1_pin1)
        self.add_combo_items("merged_pin2", cmp_pins, default=self.design_1_pin2)

    def update_host_cmp(self, sender, e):
        self.clear_combobox_items("host_pin1")
        self.clear_combobox_items("host_pin2")
        if not self.is_host_project_loaded:
            return

        cmp_pins = [str(pin.GetName())
                    for pin in self.host_edb.core_components.get_pin_from_component(sender.SelectedItem)]
        cmp_pins.sort(key=number_aware_string_key)
        self.add_combo_items("host_pin1", cmp_pins, default=self.design_2_pin1)
        self.add_combo_items("host_pin2", cmp_pins, default=self.design_2_pin2)

    def evaluate_component_placement(self, send, e):
        try:
            place_on_top, flip = self.get_place_on_top_flip()
            mounted_cmp_name = self.get_combobox_selection("combo_box_merged_cmp")
            mounted_cmp = self.merged_edb.core_components.get_component_by_name(mounted_cmp_name)
            hosting_cmp_name = self.get_combobox_selection("combo_box_host_cmp")
            hosting_cmp = self.host_edb.core_components.get_component_by_name(hosting_cmp_name)
            mounted_cmp_pin1 = self.get_combobox_selection("merged_pin1")
            mounted_cmp_pin2 = self.get_combobox_selection("merged_pin2")
            hosting_cmp_pin1 = self.get_combobox_selection("host_pin1")
            hosting_cmp_pin2 = self.get_combobox_selection("host_pin2")
            print("Host: {} {} {}".format(hosting_cmp_name, hosting_cmp_pin1, hosting_cmp_pin2))
            print("Source: {} {} {}".format(mounted_cmp_name, mounted_cmp_pin1, mounted_cmp_pin2))

            res, vector, rotation, solder_ball_height = self.host_edb.core_components. \
                get_component_placement_vector(
                mounted_component=mounted_cmp,
                hosting_component=hosting_cmp,
                mounted_component_pin1=mounted_cmp_pin1,
                mounted_component_pin2=mounted_cmp_pin2,
                hosting_component_pin1=hosting_cmp_pin1,
                hosting_component_pin2=hosting_cmp_pin2,
                flipped=flip
                )
            print("rotation before correction = {}".format(rotation))
            self.set_text_value("rotation", str(round(rotation * 180 / math.pi, 1)))
            self.set_text_value("xoffset", str(round(vector[0] * 1e3, 3)))
            self.set_text_value("yoffset", str(round(vector[1] * 1e3, 3)))
            z_pos = 0.0
            if mounted_cmp:
                z_pos = self.merged_edb.core_components.get_solder_ball_height(mounted_cmp)
                print(z_pos)
                print(self.get_combobox_selection("combo_box_host_cmp"))
            self.set_text_value("zoffset", str(round(z_pos * 1e6, 3)))
        except:
            print("no component available can't use pin for x y position")

    def get_place_on_top_flip(self):
        host_project_layer = self.get_combobox_selection("host_design_layers")
        merged_project_layer = self.get_combobox_selection("source_design_layers")
        place_on_top = True
        flip = False
        if host_project_layer == self.host_edb_bottom_layer:
            if merged_project_layer == self.source_edb_bottom_layer:
                place_on_top = False
                flip = True
            else:
                place_on_top = False
                flip = False
        else:
            if merged_project_layer == self.source_edb_bottom_layer:
                place_on_top = True
                flip = False
            else:
                place_on_top = True
                flip = True
        print("place on top = {}".format(place_on_top))
        print("flip = {}".format(flip))
        return place_on_top, flip

    def launch_merge(self, sender, e):
        if not self.are_projects_loaded:
            self.message_box("Projects not loaded!!")
        else:
            start_time = time.time()
            place_on_top, flip = self.get_place_on_top_flip()
            print("Place on top = {}".format(place_on_top))
            print("Flip merged design = {}".format(flip))
            desktop_version = self.get_text_value("desktop_version")
            pos_x = float(self.get_text_value("xoffset")) * 1e-3
            pos_y = float(self.get_text_value("yoffset")) * 1e-3
            #pos_z = float(self.get_text_value("zoffset")) * 1e-6
            pos_z = 0.0
            print("Position of Solderball")
            print(pos_z)
            rotation = float(self.get_text_value("rotation"))

            d1 = self.ui.text_value("host")
            out_edb = d1[:-5] + "_merged.aedb"
            out_project = d1[:-5] + "_merged.aedt"
            if os.path.exists(out_edb) or os.path.exists(out_project):
                i = 1
                root, _ = os.path.splitext(out_edb)
                out_edb = "{}_{}.aedb".format(root, i)
                out_project = "{}_{}.aedt".format(root, i)
                while os.path.exists(out_edb) or os.path.exists(out_project):
                    i += 1
                    out_edb = "{}_{}.aedb".format(root, i)
                    out_project = "{}_{}.aedt".format(root, i)
            d2 = self.ui.text_value("merged")
            if self.merged_edb:
                merged_project = self.merged_edb
            else:
                merged_project = Edb(edbpath=d2, edbversion=desktop_version)
            if self.host_edb:
                hosting_project = self.host_edb
            else:
                hosting_project = Edb(edbpath=d1, edbversion=desktop_version)

            result = merged_project.core_stackup.place_in_layout_3d_placement(hosting_project, angle=rotation,
                                                                                  offset_x=pos_x,
                                                                                  offset_y=pos_y, flipped_stackup=flip,
                                                                                  place_on_top=place_on_top,
                                                                                  solder_height=pos_z)
            # result = merged_project.core_stackup.place_in_layout(hosting_project, angle=rotation, offset_x=pos_x,
            #                                                          offset_y=pos_y, flipped_stackup=flip,
            #                                                          place_on_top=place_on_top)
            end_time = time.time()-start_time
            merged_project.logger.info("Placement Total Time {}".format(end_time))
            merged_project.save_edb_as(out_edb)
            merged_project.close_edb()
            hosting_project.close_edb()
            mod = sys.modules["__main__"]
            if self.get_checkbox_status("open_layout") and is_ironpython and "oDesktop" in dir(mod):
                oTool = mod.oDesktop.GetTool("ImportExport")
                oTool.ImportEDB(os.path.join(out_edb, "edb.def"))
            elif self.get_checkbox_status("open_layout"):
                hfss3d = Hfss3dLayout(os.path.join(out_edb, "edb.def"), specified_version=desktop_version)
                hfss3d.release_desktop(False, False)

            if not self.execute_merge_on_init:
                if result:
                    self.message_box("Merge completed Successfully")
                else:
                    self.message_box("Error During Merge", icon="Error")




# Launch the toolkit
if __name__ == '__main__':
    mod = sys.modules["__main__"]
    if "oDesktop" in dir(mod):
        desktop_version = mod.oDesktop.GetVersion()[0:6]
    else:
        desktop_version = None
    launch(__file__, specified_version=desktop_version, new_desktop_session=False, autosave=False)
