"""To create a Fusion script:
    Find all lines with <<<<<<<<>>>>>>>> and edit the code below


    1. Change the default_name variable in run to the name you want your
        module to show up as in the dialog box.

    2. Add the parameters you want to use to create the model using the
        parameters.addParameter() method following the format shown there.

    3. In CreatedObject.build() copy the parameters you are using into local
        variables as shown. This is not required but makes it a lot easier

    4. Write your code to create objects, do math, etc. in CreatedObject.run().
        You can add extra methods to created object to do calculations in
        CreatedObject or simply add them as functions in main

    Tips for success:

    1. Fusion is horrible at telling you what is wrong and the default mode
        if there is a error is simply to do nothing. I would highly recommend
        building in small increments and keeping Fusion open to test run the
        script very often.

    2. The Fusion documentation is sketchy at best and it is often difficult
        to figure out how features work. The documentation will tell you
        what functions exist but gives no context to what parameter
        combinations are possible, what they might be used for, or how they
        interact with eachother. Thankfully, this has led to a lot of forum
        questions being asked and these are a great resource."""


import adsk.core
import adsk.fusion
import traceback
import math
from . import fusionUtils


def run(context):
    """ The function that is run by Fusion """

    default_name = 'default' # The name which appears in the top bar
    parameters = fusionUtils.Parameters()

    """<<<<<<<<<<<<<<< Edit parameters >>>>>>>>>>>>>>>
        Parameters will apear in the order here with the following values:
        name: the varuable name that will hold the valie
        units: the units that the value will be converted to. "" for unitless
        description: the text which will appear with the box
        default_value: the initial value that will appear before being edited """

    parameters.addParameter('exampleUnitlessParameter', "", 'Unitless Parameter', 1)
    parameters.addParameter('exampleDistanceParameter', "mm", 'Distance Parameter', 4.5)


    created_object = CreatedObject() # Create an instance of the designed class
    fusionUtils.run(parameters, default_name, created_object)


class CreatedObject:
    """ The class which contains definitions to create the part """

    def __init__(self):
        self.parameters = {}

    def build(self, app, ui):
        """ Perform the features to create the component """

        newComp = fusionUtils.createNewComponent(app)
        if newComp is None:
            ui.messageBox('New component failed to create', 'New Component Failed')
            return
        
        units_mgr = app.activeProduct.unitsManager
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        root = design.rootComponent


        # <<<<<<<<<<<<<<< Copy parameters to local variables >>>>>>>>>>>>>>>
        unitless_parameter = self.parameters["exampleUnitlessParameter"]
        distance_parameter = self.parameters["exampleDistanceParameter"]



        # <<<<<<<<<<<<<<< Create features >>>>>>>>>>>>>>>


        # Some example features to use:

        # Create a component
        new_occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        new_component = new_occ.component
        new_component.name = 'New Component'



        # Create a sketch
        sk = new_component.sketches.add(root.xYConstructionPlane)



        # Draw a unit circle on the sketch offset by some value
        sketch_circles = sk.sketchCurves.sketchCircles
        center_point = adsk.core.Point3D.create(5, 0, 0)
        sketch_circles.addByCenterRadius(center_point, 1)



        # Extrude the circle to the distance component
        profile = sk.profiles.item(0)
        distance = adsk.core.ValueInput.createByReal(distance_parameter)
        extrude = new_component.features.extrudeFeatures.addSimple(profile, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)



        # Circular pattern the body
        body1 = extrude.bodies.item(0)
        body1.name = "new_body"
        inputEntites = adsk.core.ObjectCollection.create()
        inputEntites.add(body1)
        zAxis = new_component.zConstructionAxis # Axis of rotation
        # Create the input for circular pattern
        circularFeats = new_component.features.circularPatternFeatures
        circularFeatInput = circularFeats.createInput(inputEntites, zAxis)
        # Set the quantity of the elements
        circularFeatInput.quantity = adsk.core.ValueInput.createByReal(unitless_parameter)
        # Set the angle of the circular pattern
        circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        # Set symmetry of the circular pattern
        circularFeatInput.isSymmetric = True
        # Create the circular pattern
        circularFeat = circularFeats.add(circularFeatInput)


#<<<<<<<<<<<<<<< Add helper functions >>>>>>>>>>>>>>>
