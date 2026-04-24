import pybullet as p
import pybullet_data
import time

class RobotSim:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        
        self.plane = p.loadURDF("plane.urdf")
        self.robot = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)
        
    def move(self, command):
        if command == 0:
            print("Move LEFT")
            p.setJointMotorControl2(self.robot, 2, p.POSITION_CONTROL, targetPosition=-1)

        elif command == 1:
            print("Move RIGHT")
            p.setJointMotorControl2(self.robot, 2, p.POSITION_CONTROL, targetPosition=1)

        elif command == 2:
            print("FORWARD")
            p.setJointMotorControl2(self.robot, 1, p.POSITION_CONTROL, targetPosition=1)

        elif command == 3:
            print("DOWN")
            p.setJointMotorControl2(self.robot, 1, p.POSITION_CONTROL, targetPosition=-1)

        else:
            print("STOP")

        for _ in range(100):
            p.stepSimulation()
            time.sleep(1./240.)