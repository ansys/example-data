"""Helper script for Embedding Instance & Remote Session Example."""

import os

# Add static analysis
analysis = Model.AddStaticStructuralAnalysis()

# Import geometry
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import.Import(part_file_path, geometry_import_format, geometry_import_preferences)

# Assign material
matAssignment = Model.Materials.AddMaterialAssignment()
tempSel = ExtAPI.SelectionManager.CreateSelectionInfo(Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities)
bodies = [body for body in ExtAPI.DataModel.Project.Model.Geometry.GetChildren(
    Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body, True)]
geobodies = [body.GetGeoBody() for body in bodies]
tempSel.Ids = [geobody.Id for geobody in geobodies]
matAssignment.Location = tempSel
matAssignment.Material = "Structural Steel"

# Define mesh settings
mesh = Model.Mesh
mesh.ElementSize = Quantity('25 [mm]')
mesh.GenerateMesh()

# Define boundary conditions
fixedSupport = analysis.AddFixedSupport()
fixedSupport.Location = ExtAPI.DataModel.GetObjectsByName("NSFixedSupportFaces")[0]

frictionlessSupport = analysis.AddFrictionlessSupport()
frictionlessSupport.Location = ExtAPI.DataModel.GetObjectsByName("NSFrictionlessSupportFaces")[0]

pressure = analysis.AddPressure()
pressure.Location = ExtAPI.DataModel.GetObjectsByName("NSInsideFaces")[0]
inputs_quantities = [Quantity("0 [s]"), Quantity("1 [s]")]
output_quantities = [Quantity("0 [Pa]"), Quantity("15 [MPa]")]

inputs_quantities_2 = System.Collections.Generic.List[Ansys.Core.Units.Quantity]()
[inputs_quantities_2.Add(item) for item in inputs_quantities]

output_quantities_2 = System.Collections.Generic.List[Ansys.Core.Units.Quantity]()
[output_quantities_2.Add(item) for item in output_quantities]

pressure.Magnitude.Inputs[0].DiscreteValues = inputs_quantities_2
pressure.Magnitude.Output.DiscreteValues = output_quantities_2

# Solve model
Model.Solve()

# Add results
solution = analysis.Solution
solution.AddTotalDeformation()
solution.AddEquivalentStress()
solution.EvaluateAllResults()

project_dir = ExtAPI.DataModel.Project.ProjectDirectory

# Save model
ExtAPI.DataModel.Project.SaveAs(os.path.join(project_dir,'file.mechdb'))
project_dir = ExtAPI.DataModel.Project.ProjectDirectory

# Export result values to a text file
fileExtension=r".txt"
results = solution.GetChildren(Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Result,True)

for result in results:
    fileName = str(result.Name)
    path = os.path.join(project_dir,fileName+fileExtension)
    result.ExportToTextFile(True,path)