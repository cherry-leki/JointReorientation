import maya.cmds as cmds
from functools import partial

# Unbind skin (Not used)
# unbindKeepHistory=True: Keep history占쏙옙 占쏙옙占쌍억옙占? weight 占쏙옙占쏙옙 占쏙옙占쏙옙磯占?.
# skinning占쏙옙 풀占쏙옙占썽서 pose占쏙옙 占쌨띰옙占쏙옙占쏙옙占쏙옙占쏙옙 占쏙옙 占쌉쇽옙占쏙옙 占쏙옙占쏙옙占쏙옙占? 占십곤옙 占쏙옙占쏙옙.
def unbindSkinFunc():
    cmds.skinCluster('kFBXASC045modelShape', e=True, unbind=True, unbindKeepHistory=True, lw=True)
    #cmds.joint('LeftLeg', e=1, ch=1, oj='xyz', sao='yup')
    
    
# Bind skin (Not used)
# bindMethod=2: heat map 占쏙옙占쏙옙占쏙옙占? bind
def bindSkinFunc():
    cmds.select('kFBXASC045model', add=True)
    cmds.select('Hips', add=True)
    cmds.skinCluster(bindMethod=2)


# Set moveJointsMode flag in skinCluster function
# mjm = True: joints can be moved without modifying the skinning (skining占쏙옙 占쏙옙占쏙옙占쏙옙占쏙옙 占십곤옙 joint占쏙옙 占쏙옙占쏙옙 占쏙옙占쏙옙)
# After modifying joints, set the mjm=False for taking the skin out of move joints mode(joint 占쏙옙占쏙옙 占식울옙 False占쏙옙 占쏙옙占쏙옙占싹깍옙)
def setMoveJointsMode(skinModel, mode):
    #skinModel = skinModel + "Shape"
    cmds.skinCluster(skinModel, e=True, mjm=mode)
    #cmds.skinCluster('kFBXASC045modelShape', e=True, mjm=False)


# Create new skeleton
# parentJoint: current selected joint of the original skeleton
# rootJoint: the root joint of the original skeleton (aligning占쏙옙 skeleton占쏙옙 root joint)
# copyRootJoint: the root joint of the copied skeleton (占쏙옙 占쏙옙占썹를 占쏙옙占쏙옙 占쏙옙占쏙옙占쏙옙 skeleton占쏙옙 root joint)
def createChildJoint(parentJoint, rootJoint, copyRootJoint) :
    cmds.select(rootJoint, hi=True)
    cmds.select(cmds.ls(parentJoint, sl=1))
    
    for child in cmds.listRelatives(c=True):        
        # copy position of origin joint
        copyPos = cmds.xform(child, q=True, t=True, ws=True)
        
        # select parent joint in copy root
        cmds.select(copyRootJoint, hi=True)
        if parentJoint != rootJoint:
            cmds.select(cmds.ls(parentJoint + "_copied", sl=1))
        else:
            cmds.select(cmds.ls(copyRootJoint, sl=1))
        
        # create child joint
        cmds.joint(n=child + "_copied", p=copyPos)
            
        cmds.select(rootJoint, hi=True)
        if cmds.listRelatives(cmds.ls(child, sl=1), c=True):
            createChildJoint(child, rootJoint, copyRootJoint)
        
        cmds.select(d=True)
        cmds.select(rootJoint, hi=True)
        cmds.select(cmds.ls(parentJoint, sl=1))
     
    cmds.select(copyRootJoint)


# Show local axis of all joints
# showAxis: flag for showing
def showAllJointLocalAxis(showAxis, *args):
    jointList = cmds.ls(type="joint")
    for jnt in jointList:
        cmds.setAttr(jnt + ".displayLocalAxis", showAxis)


# Copy transform values of copied skeleton to original skeleton
# parentJoint: current selected joint of the original skeleton
# rootJoint: the root joint of the original skeleton (aligning占쏙옙 skeleton占쏙옙 root joint)
# copyRootJoint: the root joint of the copied skeleton (占쏙옙 占쏙옙占썹를 占쏙옙占쏙옙 占쏙옙占쏙옙占쏙옙 skeleton占쏙옙 root joint)
def copyTransformData(parentJoint, rootJoint, copyRootJoint):
    cmds.select(rootJoint, hi=True)
    cmds.select(cmds.ls(parentJoint, sl=True))
    for child in cmds.listRelatives(c=True):        
        # copy matrix of source joint
        cmds.select(copyRootJoint, hi=True)
        cmds.select(cmds.ls(child + "_copied", sl=True))
        copyMat = cmds.xform(q=True, m=True, ws=True)
        
        # set the transform matrix of copied joint to target joint
        cmds.select(rootJoint, hi=True)
        cmds.select(cmds.ls(child, sl=True))
        cmds.xform(m=copyMat, ws=True)
        # set zero rotation to target joint
        cmds.xform(ro=(0, 0, 0))
        cmds.setAttr(cmds.ls(child, sl=True)[0] + ".rotateAxis", 0, 0, 0)
        cmds.setAttr(cmds.ls(child, sl=True)[0] + ".jointOrient", 0, 0, 0)        
        
        if cmds.listRelatives(cmds.ls(child, sl=1), c=True):
            copyTransformData(child, rootJoint, copyRootJoint)


# Delete the skeleton
def deleteSkeleton(rootJoint):
    cmds.select(rootJoint, hi=True)
    cmds.delete()

# Aligning joint function for UI
def alignJointsRotAxis(rootJoint, skinModelList, *args):
    # Get root joint and skin model
    rootJoint = cmds.textField(rootJoint, q=True, tx=True)
    skinModelList = cmds.textField(skinModelList, q=True, tx=True)
    
    # Check inputs
    if not rootJoint:
        print("*Input the root joint")
        return
    if not skinModelList:
        print("*Input the skin model")
        return
        
    skinModelList = skinModelList.split(',')
    
    # Aligning process
    cmds.select(d=True)
    # Copy root joint
    rootPos = cmds.xform(rootJoint, q=True, t=True, ws=True)    
    copyRoot = cmds.joint(n=rootJoint + "_copied", p=rootPos)
    copyRootName = cmds.ls(copyRoot)[0]
            
    # Call createChildJoint
    root = cmds.ls(rootJoint)[0]
    createChildJoint(root, rootJoint, copyRootName)
    
    print("=== Copying the skeleton is done ===")
    
    # Copy source skeleton transformation to target skeleton
    for skinModel in skinModelList:
        setMoveJointsMode(skinModel, True)
    cmds.xform(rootJoint, m=cmds.xform(copyRootName, q=True, m=True, ws=True), ws=True)
    cmds.xform(rootJoint, ro=(0, 0, 0))
    cmds.setAttr(rootJoint + '.jointOrient', 0, 0, 0)
    cmds.setAttr(rootJoint + '.rotateAxis', 0, 0, 0)
    copyTransformData(root, rootJoint, copyRootName)
    for skinModel in skinModelList:
        setMoveJointsMode(skinModel, False)
    
    print("=== Aligning the original skeleton is done ===")
    
    # delete copied skeleton
    deleteSkeleton(copyRootName)


# Rotate joint function in object mode
def rotateJoint(selectedJoint, rotX, rotY, rotZ, *args):
    selectedJoint = cmds.textField(selectedJoint, q=True, tx=True)
    rotX = cmds.textField(rotX, q=True, tx=True)
    rotY = cmds.textField(rotY, q=True, tx=True)
    rotZ = cmds.textField(rotZ, q=True, tx=True)
    
    if not selectedJoint:
        print("*Input the joint name")
        return
        
    if not rotX or not rotY or not rotZ:
        print("*Input the rotate values")
        return
    
    cmds.selectMode(object=True)
    cmds.hilite(selectedJoint)
    cmds.select(selectedJoint + '.rotateAxis', replace=True)
    cmds.rotate(rotX, rotY, rotZ, relative=True, objectSpace=True, forceOrderXYZ=True)


# UI for aligning joint rotation
def alignmentUI():
    windowName = "Joint rotation axis controller"
    windowSize = [310, 330]
    window = cmds.window(title=windowName, widthHeight=windowSize, sizeable=False)

    cmds.columnLayout("mainLayout")
    cmds.text(label=" ",h=3)
    
    # Display all local joint axis
    cmds.text(label="Display local axis of all joints", fn="boldLabelFont")
    cmds.rowLayout("displayAxesLayout", p="mainLayout", numberOfColumns=2, h=35)
    cmds.text(label="Display local axis   ", p="displayAxesLayout")
    cmds.checkBox(label="", p="displayAxesLayout",
                  onCommand=partial(showAllJointLocalAxis, True), offCommand=partial(showAllJointLocalAxis, False))
    
    cmds.separator(w=windowSize[0], h=30, p="mainLayout")
    
    # Align all joint's z-axis to forward direction
    cmds.text(label="Align all joint's z-axis to forward direction", fn="boldLabelFont", p="mainLayout")
    cmds.text(label=" ", h=3, p="mainLayout")
    # Setting root joint
    cmds.rowLayout("rootJointLayout", p="mainLayout", numberOfColumns=2)
    cmds.text(label="Input root joint: ", p="rootJointLayout", w=90, align="left")
    rootJoint = cmds.textField(tx="Hips", p="rootJointLayout", w=150)
    # Setting skin model
    cmds.rowLayout("skinLayout", p="mainLayout", numberOfColumns=2)
    cmds.text(label="Input skin model: ", p="skinLayout", w=90, align="left")
    skinModel = cmds.textField(tx="kFBXASC045model", p="skinLayout", w=150)
    # Aligning button
    cmds.button(label="Align joints", w=windowSize[0], h=50, p="mainLayout", command=partial(alignJointsRotAxis, rootJoint, skinModel))
    
    cmds.separator(w=windowSize[0], h=30, p="mainLayout")
    
    # Rotate certain joint
    cmds.text(label="Rotate the joint in object mode", fn="boldLabelFont", p="mainLayout")
    cmds.text(label=" ", h=3, p="mainLayout")
    cmds.rowLayout("selectedJointLayout", p="mainLayout", numberOfColumns=8)
    # Setting selected joint
    cmds.text(label="Input joint: ", p="selectedJointLayout")
    selectedJoint = cmds.textField(p="selectedJointLayout")
    # Setting rotate values
    cmds.text(label="x: ", p="selectedJointLayout", w=25, align="right")
    rotX = cmds.textField(tx="0", p="selectedJointLayout", w=30)
    cmds.text(label="y: ", p="selectedJointLayout")
    rotY = cmds.textField(tx="0", p="selectedJointLayout", w=30)
    cmds.text(label="z: ", p="selectedJointLayout")
    rotZ = cmds.textField(tx="0", p="selectedJointLayout", w=30)
    # Rotating button
    cmds.button(label="Rotate joint", w=windowSize[0], h=50, p="mainLayout", command=partial(rotateJoint, selectedJoint, rotX, rotY, rotZ))

    cmds.showWindow(window)
    

''' Main '''
if __name__ == "__main__":
    alignmentUI()
