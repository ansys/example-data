import math
import os
import time

from pyaedt import Edb, Hfss3dLayout
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
            desktop_version= config.get("desktop_version", "2021.2")
            host = config.get("host","")
            if host and not os.path.exists(os.path.join(os.path.dirname(__file__), host)):
                host = os.path.join(os.path.dirname(__file__), host)
            merge =  config.get("merge","")
            if merge and not os.path.exists(os.path.join(os.path.dirname(__file__), host)):
                merge = os.path.join(os.path.dirname(__file__), merge)
            self.load_layout_on_init = config.get("load_layout_on_init", "0") == "1"
            self.host_component = config.get("host_component", None)
            self.merge_component = config.get("merge_component", None)
            self.design_1_pin1 = config.get("design_1_pin1", None)
            self.design_1_pin2 = config.get("design_1_pin2", None)
            self.design_2_pin1 = config.get("design_2_pin1", None)
            self.design_2_pin2 = config.get("design_2_pin2", None)
            xoffset = config.get("xoffset", "0.0")
            yoffset = config.get("yoffset", "0.0")
            zoffset = config.get("zoffset", "0.0")
            rotation = config.get("rotation", "0")
            flip_layout = config.get("flip_layout", "0") == "1"
            place_on_top = config.get("place_on_top", "0") == "1"
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
            place_on_top = True
            open_3d_layout = False
            placement_3d = False
            self.evaluate_placement_on_init = False
            self.execute_merge_on_init = False
        self.valid_project = True
        self.design1_edb = None
        self.design2_edb = None
        self.copy_xaml_template()
        self.edit_window_size(900, 400, "Pyaedt EDB Merge Utility")
        #Edit the UI
        self.add_label("label1", "Merged Layout", 10, 10)
        self.add_text_box(name="merged", x_pos=150, y_pos=10, width=400)
        self.add_button("merged_path_button", "Browse...", x_pos=600,  y_pos=10, callback_method=self.browse_design1)

        self.add_label("label2", "Host Layout", 10, 50)
        self.add_text_box(name="host", x_pos=150, y_pos=50, width=400)
        self.add_button("host_path_button", "Browse...", x_pos=600,  y_pos=50, callback_method=self.browse_design2)

        self.add_label("label7", "Desktop Version", 10, 130)
        self.add_text_box(name="desktop_version", x_pos=200, y_pos=130, callback_method=self.validate_string_no_spaces,
                          callback_action='LostFocus')

        self.add_label("label4", "Rotation (deg)", 10, 160)
        self.add_text_box(name="rotation", x_pos=200, y_pos=160, callback_method=self.validate_float,
                          callback_action='LostFocus')

        self.add_label("label5", "X Offset (mm)", 10, 190)
        self.add_text_box(name="xoffset", x_pos=200, y_pos=190, callback_method=self.validate_float,
                          callback_action='LostFocus')

        self.add_label("label6", "Y Offset (mm)", 10, 220)
        self.add_text_box(name="yoffset", x_pos=200, y_pos=220, callback_method=self.validate_float,
                          callback_action='LostFocus')

        self.add_label("label3", "Optional Solder ball height (um)", 10, 250)
        self.add_text_box(name="zoffset", x_pos=200, y_pos=250, callback_method=self.validate_float,
                          callback_action='LostFocus')

        self.add_button("load_layout_button", "Load project", x_pos=600, y_pos=90, callback_method=self.load_layout)
        self.add_check_box("placement_3d", "3d Placement", x_pos=100, y_pos=280)

        self.add_button("execute_button", "Merged layout", x_pos=200, y_pos=280, callback_method=self.launch_merge)
        self.add_button("evaluate_vector_button", "Evaluate placement", x_pos=600, y_pos=130,
                        callback_method=self.evaluate_component_placement)


        self.add_label("label36", "Merged Component", 350, 160)
        self.add_combo_box("combo_box_merged_cmp", x_pos=350, y_pos=185, callback_action='SelectionChanged',
                           callback_method=self.update_merged_cmp)
        self.add_label("label17", "Host Component", 350, 205)
        self.add_combo_box("combo_box_host_cmp", x_pos=350, y_pos=230, callback_action='SelectionChanged',
                           callback_method=self.update_host_cmp)

        self.add_check_box("place_on_top_check", "Place on top", x_pos=350, y_pos=100)
        self.add_check_box("flip_check", "Flip merged design before placing", x_pos=350, y_pos=120)
        self.add_check_box("open_layout", "Open 3d Layout after merge", x_pos=350, y_pos=140)

        self.add_label("label_pin_matching", "Pin matching", 600, 160)
        self.add_label("merge_1_pins", "Host", 530, 205)
        self.add_combo_box("merged_pin1", x_pos=500, y_pos=185)
        self.add_combo_box("merged_pin2", x_pos=500, y_pos=230)

        self.add_label("host_2_pins", "Merged", 680, 205)
        self.add_combo_box("host_pin1", x_pos=650, y_pos=185)
        self.add_combo_box("host_pin2", x_pos=650, y_pos=230)

        self.launch_gui()

        self.set_text_value("desktop_version", desktop_version)
        self.set_text_value("merged", merge)
        self.set_text_value("host", host)
        self.set_text_value("rotation", rotation)
        self.set_text_value("xoffset", xoffset)
        self.set_text_value("yoffset", yoffset)
        self.set_text_value("zoffset", zoffset)
        self.set_chechbox_status("place_on_top_check", place_on_top)
        self.set_chechbox_status("placement_3d",placement_3d )
        self.set_chechbox_status("flip_check",flip_layout)
        self.set_chechbox_status("open_layout", open_3d_layout)
        if self.load_layout_on_init:
            self.load_layout(None, None)
            if self.evaluate_placement_on_init:
                self.evaluate_component_placement(None, None)
            if self.execute_merge_on_init:
                self.launch_merge(None, None)

    def load_layout(self, sender, e):
        if os.path.isdir(self.ui.text_value("merged")):
            self.merged_edb = Edb(edbpath=self.ui.text_value("merged"), edbversion="2021.2")
        else:
            self.valid_project = False
            self.message_box("Failed to load design {}".format(self.ui.text_value("merged")), icon="Error")
        if os.path.isdir(self.ui.text_value("host")):
            self.host_edb = Edb(edbpath=self.ui.text_value("host"), edbversion="2021.2")
        else:
            self.valid_project = False
            self.message_box("Failed to load design {}".format(self.ui.text_value("host")), icon="Error")

        if self.valid_project:
            design1_components = [str(i) for i in list(self.merged_edb.core_components.components.keys())]
            if design1_components:
                self.add_combo_items("combo_box_merged_cmp", design1_components, default=self.merge_component)
            design2_components = [str(i) for i in list(self.host_edb.core_components.components.keys())]

            if design2_components:
                self.add_combo_items("combo_box_host_cmp", design2_components, default=self.host_component)
            if not self.load_layout_on_init:
                self.message_box("Models Loaded correctly")


    def browse_design1(self, sender, e):
        aedb_folder = select_directory(description="Merged Aedb Path")
        self.set_text_value("merged", aedb_folder)

    def browse_design2(self, sender, e):
        aedb_folder = select_directory(description="Host Aedb Path")
        self.set_text_value("host", aedb_folder)

    def enable_checkbox(self, sender, e):
        print("Enabled")

    def disable_checkbox(self, sender, e):
        print("Disabled")

    def aedt_add_log(self, text):
        self.aedtdesign.logger.info(text)

    def update_merged_cmp(self, sender, e):

        cmp_pins = [str(pin.GetName())
                    for pin in self.merged_edb.core_components.get_pin_from_component(sender.SelectedItem)]
        self.clear_combobox_items("merged_pin1")
        self.clear_combobox_items("merged_pin2")
        self.add_combo_items("merged_pin1", cmp_pins, default=self.design_1_pin1)
        self.add_combo_items("merged_pin2", cmp_pins, default=self.design_1_pin2)

    def update_host_cmp(self, sender, e):

        cmp_pins = [str(pin.GetName())
                    for pin in self.host_edb.core_components.get_pin_from_component(sender.SelectedItem)]
        self.clear_combobox_items("host_pin1")
        self.clear_combobox_items("host_pin2")
        self.add_combo_items("host_pin1", cmp_pins, default=self.design_2_pin1)
        self.add_combo_items("host_pin2", cmp_pins, default=self.design_2_pin2)

    def evaluate_component_placement(self, send, e):
        try:
            mounted_cmp = self.merged_edb.core_components. \
                get_component_by_name(self.get_combobox_selection("combo_box_merged_cmp"))
            hosting_cmp = self.host_edb.core_components. \
                get_component_by_name(self.get_combobox_selection("combo_box_host_cmp"))
            mounted_cmp_pin1 = self.get_combobox_selection("merged_pin1")
            mounted_cmp_pin2 = self.get_combobox_selection("merged_pin2")
            hosting_cmp_pin1 = self.get_combobox_selection("host_pin1")
            hosting_cmp_pin2 = self.get_combobox_selection("host_pin2")
            res, vector, rotation, solder_ball_height = self.host_edb.core_components. \
                get_component_placement_vector(
                mounted_component=mounted_cmp,
                hosting_component=hosting_cmp,
                mounted_component_pin1=mounted_cmp_pin1,
                mounted_component_pin2=mounted_cmp_pin2,
                hosting_component_pin1=hosting_cmp_pin1,
                hosting_component_pin2=hosting_cmp_pin2)
            self.set_text_value("rotation", str(round(rotation * 180 / math.pi, 3)))
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



    def launch_merge(self, sender, e):
        start_time = time.time()
        flip = self.get_checkbox_status("flip_check")
        place_on_top = self.get_checkbox_status("place_on_top_check")
        desktop_version = self.get_text_value("desktop_version")
        pos_x = float(self.get_text_value("xoffset")) * 1e-3
        pos_y = float(self.get_text_value("yoffset")) * 1e-3
        pos_z = float(self.get_text_value("zoffset")) * 1e-6
        print("Position of Solderball")
        print(pos_z)
        rotation = float(self.get_text_value("rotation"))

        d1 = self.ui.text_value("host")
        d2 = self.ui.text_value("merged")
        if self.merged_edb:
            merged_project = self.merged_edb
        else:
            merged_project = Edb(edbpath=d2, edbversion=desktop_version)
        if self.host_edb:
            hosting_project = self.host_edb
        else:
            hosting_project = Edb(edbpath=d1, edbversion=desktop_version)

        out_project = d1[:-5] + "_merged.aedb"
        if self.get_checkbox_status("placement_3d"):
            result = merged_project.core_stackup.place_in_layout_3d_placement(hosting_project, angle=rotation,
                                                                              offset_x=pos_x,
                                                                              offset_y=pos_y, flipped_stackup=flip,
                                                                              place_on_top=place_on_top,
                                                                              solder_height=pos_z)
        else:
            result = merged_project.core_stackup.place_in_layout(hosting_project, angle=rotation, offset_x=pos_x,
                                                                 offset_y=pos_y, flipped_stackup=flip,
                                                                 place_on_top=place_on_top)
        end_time = time.time()-start_time
        merged_project.logger.info("Placement Total Time {}".format(end_time))
        merged_project.save_edb_as(out_project)
        merged_project.close_edb()
        hosting_project.close_edb()
        if self.get_checkbox_status("open_layout"):
            hfss3d = Hfss3dLayout(os.path.join(out_project, "edb.def"),specified_version=desktop_version)
            hfss3d.release_desktop(False, False)
        if not self.execute_merge_on_init:
            if result:
                self.message_box("Merge completed Successfully")
            else:
                self.message_box("Error During Merge",icon="Error")




# Launch the toolkit
if __name__ == '__main__':
    launch(__file__, specified_version="2021.2", new_desktop_session=False, autosave=False)
