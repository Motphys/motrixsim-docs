from legged_gym.addr import LEGGED_GYM_ENVS_DIR
from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg


class BHCfg(LeggedRobotCfg):  # policy_biped_50hz
    # control_dt: 0.004
    # policy_dt: 0.02
    class sim(LeggedRobotCfg.sim):
        dt = 0.004

    class env(LeggedRobotCfg.env):
        num_observations = 45

    class control(LeggedRobotCfg.control):
        action_scale = 0.25
        decimation = 5
        stiffness = 20
        damping = 2
        torque_limits = 5

    class init_state(LeggedRobotCfg.init_state):
        default_joint_angles = {  # = target angles [rad] when action = 0.0
            "leg_left_hip_roll_joint": 0.0,
            "leg_left_hip_yaw_joint": 0.0,
            "leg_left_hip_pitch_joint": -0.2,
            "leg_left_knee_pitch_joint": 0.4,
            "leg_left_ankle_pitch_joint": -0.3,
            "leg_left_ankle_roll_joint": 0.0,
            "leg_right_hip_roll_joint": 0.0,
            "leg_right_hip_yaw_joint": 0.0,
            "leg_right_hip_pitch_joint": -0.2,
            "leg_right_knee_pitch_joint": 0.4,
            "leg_right_ankle_pitch_joint": -0.3,
            "leg_right_ankle_roll_joint": 0.0,
        }

    class asset(LeggedRobotCfg.asset):
        file = LEGGED_GYM_ENVS_DIR + "/resources/robots/BHL/bhl_biped_scene.xml"
        body_name = "base"

    class sensor(LeggedRobotCfg.sensor):
        gyro = "imu_gyro"

    class commands(LeggedRobotCfg.commands):
        class ranges(LeggedRobotCfg.commands.ranges):
            lin_vel_x = [-1.5, 1.5]  # min max [m/s]
            lin_vel_y = [-1, 1]  # min max [m/s]
            ang_vel_yaw = [-0.5, 0.5]  # min max [rad/s]
            heading = [-3.14, 3.14]
