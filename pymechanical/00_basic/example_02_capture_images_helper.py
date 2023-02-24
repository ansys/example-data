import os

# the following needs to be set
# image_dir - path where images need to be saved
# mechdat_path - path to example_03_simple_bolt_new.mechdat

ExtAPI.DataModel.Project.Open(mechdat_path)

#Add results for the bolt model based on tags
# Get the number of steps for the analysis
analysisSettings = Model.Analyses[0].AnalysisSettings
numSteps = analysisSettings.NumberOfSteps

solution = Model.Analyses[0].Solution
bolt = DataModel.GetObjectsByName("Bolt")[0]

# Create tags that we will use later for finding objects
Tags = ExtAPI.DataModel.ObjectTags
Tag1 = Ansys.Mechanical.Application.ObjectTag ("AllBodies")
Tag2 = Ansys.Mechanical.Application.ObjectTag ("Bolt")
Tag3 = Ansys.Mechanical.Application.ObjectTag ("U Sum")
Tag4 = Ansys.Mechanical.Application.ObjectTag ("EQV")
Tags.Add(Tag1)
Tags.Add(Tag2)
Tags.Add(Tag3)
Tags.Add(Tag4)

# For each step add the desired result objects with appropriate settings
for step in range(1,numSteps):
    resultU = solution.AddTotalDeformation()
    resultU.Name = "Total Deformation @ " + str(step) + " sec"
    resultU.DisplayTime = analysisSettings.GetStepEndTime(step)
    Tag1.AddObject(resultU)
    Tag3.AddObject(resultU)

    resultS = solution.AddEquivalentStress()
    resultS.Name = "Eqv Stress @ " + str(step) + " sec"
    Tag1.AddObject(resultS)
    Tag4.AddObject(resultS)

for step in range(1,numSteps):
    resultU = solution.AddTotalDeformation()
    resultU.Name = "Bolt Deformation @ " + str(step) + " sec"
    resultU.Location = bolt
    resultU.DisplayTime = analysisSettings.GetStepEndTime(step)
    resultU.CalculateTimeHistory = False
    Tag2.AddObject(resultU)
    Tag3.AddObject(resultU)

    resultS = solution.AddEquivalentStress()
    resultS.Name = "Bolt Stress @ " + str(step) + " sec"
    resultS.Location = bolt
    Tag2.AddObject(resultS)
    Tag4.AddObject(resultS)

tag1_list = Tag1.Objects
tag2_list = Tag2.Objects
tag3_list = Tag3.Objects
tag4_list = Tag4.Objects

# Find similar objects using the tags
uAll = [x for x in tag3_list if x not in tag2_list]
uBolt = [x for x in tag3_list if x in tag2_list]
sAll = [x for x in tag4_list if x not in tag2_list]
sBolt = [x for x in tag4_list if x in tag2_list]

# Group similar objects
group = Tree.Group(uAll)
group.Name = "Total Deformation (All Bodies)"
group = Tree.Group(uBolt)
group.Name = "Total Deformation (Bolt)"
group = Tree.Group(sAll)
group.Name = "Stress (All Bodies)"
group = Tree.Group(sBolt)
group.Name = "Stress (Bolt)"

solution.Activate()
solution.ClearGeneratedData()
solution.Solve(True)

# Set custom legend
for analysis in Model.Analyses:
    results = analysis.Solution.GetChildren(DataModelObjectCategory.Result, True)
    for result in results:
        result.Activate()
        legendSettings = Ansys.Mechanical.Graphics.Tools.CurrentLegendSettings()
        legendSettings.SetBandColor(0, Ansys.Mechanical.DataModel.Constants.Colors.Gray)

# Create images with specific orientation and store on disk
#Visit the first result, otherwise images are not good
DataModel.GetObjectsByName(Model.Analyses[0].Solution.GetChildren(DataModelObjectCategory.Result, True)[0].Name)[0].Activate()

#Set camera and view
#cam = Graphics.Camera
#cam.SetSpecificViewOrientation(ViewOrientationType.Right)
#cam.SetFit()
#cam.Rotate(90, CameraAxisType.GlobalY)

# Set camera properties
Graphics.Camera.FocalPoint = Point([3.600663, -0.621037, 0.548997], 'm')
Graphics.Camera.ViewVector = Vector3D(1, 0, 0)
Graphics.Camera.UpVector = Vector3D(0, 1, 3.46945e-17)
Graphics.Camera.SceneHeight = Quantity(0.186285, 'm')
Graphics.Camera.SceneWidth = Quantity(0.277377, 'm')

for analysis in Model.Analyses:
    results = analysis.Solution.GetChildren(DataModelObjectCategory.Result, True)
    for result in results:
        DataModel.GetObjectsByName(result.Name)[0].Activate()

        #Image to file settings
        set2d = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
        set2d.CurrentGraphicsDisplay = False

        pathvar = os.path.join(image_dir, result.Name)
        Graphics.ExportImage(pathvar + "_" + "Right" + ".png", GraphicsImageExportFormat.PNG, set2d)

# Exporting a result animation to wmv video file with given resolution, frames and duration
Graphics.ResultAnimationOptions.NumberOfFrames = 10
Graphics.ResultAnimationOptions.Duration = Quantity(2, 's')
settings = Ansys.Mechanical.Graphics.AnimationExportSettings(width = 1000, height = 665)

result = Tree.FirstActiveObject
pathvar = os.path.join(image_dir, result.Name)
result.ExportAnimation(pathvar + ".wmv",GraphicsAnimationExportFormat.WMV,settings)

