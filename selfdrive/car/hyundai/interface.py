#!/usr/bin/env python3
from cereal import car
from selfdrive.config import Conversions as CV
from selfdrive.car.hyundai.values import Ecu, ECU_FINGERPRINT, CAR, FINGERPRINTS, Buttons
from selfdrive.car import STD_CARGO_KG, scale_rot_inertia, scale_tire_stiffness, is_ecu_disconnected, gen_empty_fingerprint
from selfdrive.car.interfaces import CarInterfaceBase, MAX_CTRL_SPEED
from common.params import Params
from selfdrive.kyd_conf import kyd_conf

EventName = car.CarEvent.EventName
ButtonType = car.CarState.ButtonEvent.Type

class CarInterface(CarInterfaceBase):
  def __init__(self, CP, CarController, CarState):
    super().__init__(CP, CarController, CarState )
    self.cp2 = self.CS.get_can2_parser(CP)
    
  @staticmethod
  def compute_gb(accel, speed):
    return float(accel) / 3.0

  @staticmethod
  def get_params(candidate, fingerprint=gen_empty_fingerprint(), has_relay=False, car_fw=[]):  # pylint: disable=dangerous-default-value
    ret = CarInterfaceBase.get_std_params(candidate, fingerprint, has_relay)

    ret.carName = "hyundai"
    ret.safetyModel = car.CarParams.SafetyModel.hyundai

    params = Params()
    if int(params.get('LateralControlPriority')) == 0:
      ret.radarOffCan = False   #False(선행차우선)  #True(차선우선)    #선행차량 인식 마크 유무.
    else:
      ret.radarOffCan = True

    # Most Hyundai car ports are community features for now
    ret.communityFeature = False

    kyd = kyd_conf()
    tire_stiffness_factor = 1.
    ret.steerActuatorDelay = float(kyd.conf['SteerActuatorDelay'])  # 0.3
    ret.steerRateCost = 0.5
    ret.steerLimitTimer = float(kyd.conf['SteerLimitTimer'])  # 0.4

    if int(params.get('LateralControlMethod')) == 0:
      if candidate == CAR.SANTAFE:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1830. + STD_CARGO_KG
        ret.wheelbase = 2.765
        # Values from optimizer
        ret.steerRatio = 13.8  # 13.8 is spec end-to-end
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.SORENTO:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1950. + STD_CARGO_KG
        ret.wheelbase = 2.78
        ret.steerRatio = 14.4 * 1.15
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.GENESIS:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 2060. + STD_CARGO_KG
        ret.wheelbase = 3.01
        ret.steerRatio = 16.5
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.16], [0.01]]
      elif candidate in [CAR.K5, CAR.SONATA]:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1470. + STD_CARGO_KG
        ret.wheelbase = 2.80
        ret.steerRatio = 12.75
        ret.steerRateCost = 0.4
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.SONATA_TURBO:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1565. + STD_CARGO_KG
        ret.wheelbase = 2.80
        ret.steerRatio = 14.4 * 1.15   # 15% higher at the center seems reasonable
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate in [CAR.K5_HEV, CAR.SONATA_HEV]:
        ret.lateralTuning.pid.kf = 0.00006
        ret.mass = 1595. + STD_CARGO_KG
        ret.wheelbase = 2.80
        ret.steerRatio = 12.75
        ret.steerRateCost = 0.4
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate in [CAR.GRANDEUR, CAR.K7]:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1570. + STD_CARGO_KG
        ret.wheelbase = 2.885
        ret.steerRatio = 12.5
        ret.steerRateCost = 0.4
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate in [CAR.GRANDEUR_HEV, CAR.K7_HEV]:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1675. + STD_CARGO_KG
        ret.wheelbase = 2.885
        ret.steerRatio = 12.5
        ret.steerRateCost = 0.4
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.STINGER:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1825. + STD_CARGO_KG
        ret.wheelbase = 2.78
        ret.steerRatio = 14.4 * 1.15   # 15% higher at the center seems reasonable
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.KONA:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1330. + STD_CARGO_KG
        ret.wheelbase = 2.6
        ret.steerRatio = 13.5   #Spec
        ret.steerRateCost = 0.4
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.KONA_HEV:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1330. + STD_CARGO_KG
        ret.wheelbase = 2.6
        ret.steerRatio = 13.5   #Spec
        ret.steerRateCost = 0.4
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.KONA_EV:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1330. + STD_CARGO_KG
        ret.wheelbase = 2.6
        ret.steerRatio = 13.5   #Spec
        ret.steerRateCost = 0.4
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.NIRO_HEV:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1425. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.73   #Spec
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.NIRO_EV:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1425. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.73   #Spec
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.IONIQ_HEV:
        ret.lateralTuning.pid.kf = 0.00006
        ret.mass = 1275. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.73   #Spec
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.IONIQ_EV:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1490. + STD_CARGO_KG   #weight per hyundai site https://www.hyundaiusa.com/ioniq-electric/specifications.aspx
        ret.wheelbase = 2.7
        ret.steerRatio = 13.25   #Spec
        ret.steerRateCost = 0.4
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.NEXO:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1885. + STD_CARGO_KG
        ret.wheelbase = 2.79
        ret.steerRatio = 12.5
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.MOHAVE:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 2250. + STD_CARGO_KG
        ret.wheelbase = 2.895
        ret.steerRatio = 14.1
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.I30:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1380. + STD_CARGO_KG
        ret.wheelbase = 2.65
        ret.steerRatio = 13.5
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.AVANTE:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1275. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.5            # 14 is Stock | Settled Params Learner values are steerRatio: 15.401566348670535
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.SELTOS:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1470. + STD_CARGO_KG
        ret.wheelbase = 2.63
        ret.steerRatio = 13.0
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      elif candidate == CAR.PALISADE:
        ret.lateralTuning.pid.kf = 0.00005
        ret.mass = 1955. + STD_CARGO_KG
        ret.wheelbase = 2.90
        ret.steerRatio = 13.0
        ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
        ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif int(params.get('LateralControlMethod')) == 1:
      if candidate == CAR.SANTAFE:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1830. + STD_CARGO_KG
        ret.wheelbase = 2.765
        ret.steerRatio = 13.8  # 13.8 is spec end-to-end
      elif candidate == CAR.SORENTO:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1950. + STD_CARGO_KG
        ret.wheelbase = 2.78
        ret.steerRatio = 14.4 * 1.15
      elif candidate == CAR.GENESIS:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 2060. + STD_CARGO_KG
        ret.wheelbase = 3.01
        ret.steerRatio = 16.5
      elif candidate in [CAR.K5, CAR.SONATA]:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1470. + STD_CARGO_KG
        ret.wheelbase = 2.80
        ret.steerRatio = 12.75
        ret.steerRateCost = 0.4
      elif candidate == CAR.SONATA_TURBO:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1565. + STD_CARGO_KG
        ret.wheelbase = 2.80
        ret.steerRatio = 14.4 * 1.15   # 15% higher at the center seems reasonable
      elif candidate in [CAR.K5_HEV, CAR.SONATA_HEV]:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1595. + STD_CARGO_KG
        ret.wheelbase = 2.80
        ret.steerRatio = 12.75
        ret.steerRateCost = 0.4
      elif candidate in [CAR.GRANDEUR, CAR.K7]:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1570. + STD_CARGO_KG
        ret.wheelbase = 2.885
        ret.steerRatio = 12.5
        ret.steerRateCost = 0.4
      elif candidate in [CAR.GRANDEUR_HEV, CAR.K7_HEV]:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1675. + STD_CARGO_KG
        ret.wheelbase = 2.885
        ret.steerRatio = 12.5
        ret.steerRateCost = 0.4
      elif candidate == CAR.STINGER:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1825. + STD_CARGO_KG
        ret.wheelbase = 2.78
        ret.steerRatio = 14.4 * 1.15   # 15% higher at the center seems reasonable
      elif candidate == CAR.KONA:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1330. + STD_CARGO_KG
        ret.wheelbase = 2.6
        ret.steerRatio = 13.5   #Spec
        ret.steerRateCost = 0.4
      elif candidate == CAR.KONA_HEV:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1330. + STD_CARGO_KG
        ret.wheelbase = 2.6
        ret.steerRatio = 13.5   #Spec
        ret.steerRateCost = 0.4
      elif candidate == CAR.KONA_EV:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1330. + STD_CARGO_KG
        ret.wheelbase = 2.6
        ret.steerRatio = 13.5   #Spec
        ret.steerRateCost = 0.4
      elif candidate == CAR.NIRO_HEV:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1425. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.73   #Spec
      elif candidate == CAR.NIRO_EV:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1425. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.73   #Spec
      elif candidate == CAR.IONIQ_HEV:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1275. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.73   #Spec
      elif candidate == CAR.IONIQ_EV:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1490. + STD_CARGO_KG   #weight per hyundai site https://www.hyundaiusa.com/ioniq-electric/specifications.aspx
        ret.wheelbase = 2.7
        ret.steerRatio = 13.25   #Spec
        ret.steerRateCost = 0.4
      elif candidate == CAR.NEXO:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1885. + STD_CARGO_KG
        ret.wheelbase = 2.79
        ret.steerRatio = 12.5
      elif candidate == CAR.MOHAVE:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 2250. + STD_CARGO_KG
        ret.wheelbase = 2.895
        ret.steerRatio = 14.1
      elif candidate == CAR.I30:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1380. + STD_CARGO_KG
        ret.wheelbase = 2.65
        ret.steerRatio = 13.5
      elif candidate == CAR.AVANTE:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1275. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.5            # 14 is Stock | Settled Params Learner values are steerRatio: 15.401566348670535
      elif candidate == CAR.SELTOS:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1470. + STD_CARGO_KG
        ret.wheelbase = 2.63
        ret.steerRatio = 13.0
      elif candidate == CAR.PALISADE:
        ret.lateralTuning.init('indi')
        ret.lateralTuning.indi.innerLoopGain = 3.0
        ret.lateralTuning.indi.outerLoopGain = 2.0
        ret.lateralTuning.indi.timeConstant = 1.0
        ret.lateralTuning.indi.actuatorEffectiveness = 1.5
        ret.mass = 1955. + STD_CARGO_KG
        ret.wheelbase = 2.90
        ret.steerRatio = 13.0
    elif int(params.get('LateralControlMethod')) == 2:
      if candidate == CAR.SANTAFE:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1830. + STD_CARGO_KG
        ret.wheelbase = 2.765
        ret.steerRatio = 13.8  # 13.8 is spec end-to-end
      elif candidate == CAR.SORENTO:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1950. + STD_CARGO_KG
        ret.wheelbase = 2.78
        ret.steerRatio = 14.4 * 1.15
      elif candidate == CAR.GENESIS:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 2060. + STD_CARGO_KG
        ret.wheelbase = 3.01
        ret.steerRatio = 16.5
      elif candidate in [CAR.K5, CAR.SONATA]:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1470. + STD_CARGO_KG
        ret.wheelbase = 2.80
        ret.steerRatio = 12.75
        ret.steerRateCost = 0.4
      elif candidate == CAR.SONATA_TURBO:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1565. + STD_CARGO_KG
        ret.wheelbase = 2.80
        ret.steerRatio = 14.4 * 1.15   # 15% higher at the center seems reasonable
      elif candidate in [CAR.K5_HEV, CAR.SONATA_HEV]:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1595. + STD_CARGO_KG
        ret.wheelbase = 2.80
        ret.steerRatio = 12.75
        ret.steerRateCost = 0.4
      elif candidate in [CAR.GRANDEUR, CAR.K7]:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1570. + STD_CARGO_KG
        ret.wheelbase = 2.885
        ret.steerRatio = 12.5
        ret.steerRateCost = 0.4
      elif candidate in [CAR.GRANDEUR_HEV, CAR.K7_HEV]:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1675. + STD_CARGO_KG
        ret.wheelbase = 2.885
        ret.steerRatio = 12.5
        ret.steerRateCost = 0.4
      elif candidate == CAR.STINGER:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1825. + STD_CARGO_KG
        ret.wheelbase = 2.78
        ret.steerRatio = 14.4 * 1.15   # 15% higher at the center seems reasonable
      elif candidate == CAR.KONA:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1330. + STD_CARGO_KG
        ret.wheelbase = 2.6
        ret.steerRatio = 13.5   #Spec
        ret.steerRateCost = 0.4
      elif candidate == CAR.KONA_HEV:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1330. + STD_CARGO_KG
        ret.wheelbase = 2.6
        ret.steerRatio = 13.5   #Spec
        ret.steerRateCost = 0.4
      elif candidate == CAR.KONA_EV:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1330. + STD_CARGO_KG
        ret.wheelbase = 2.6
        ret.steerRatio = 13.5   #Spec
        ret.steerRateCost = 0.4
      elif candidate == CAR.NIRO_HEV:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1425. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.73   #Spec
      elif candidate == CAR.NIRO_EV:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1425. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.73   #Spec
      elif candidate == CAR.IONIQ_HEV:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1275. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.73   #Spec
      elif candidate == CAR.IONIQ_EV:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1490. + STD_CARGO_KG   #weight per hyundai site https://www.hyundaiusa.com/ioniq-electric/specifications.aspx
        ret.wheelbase = 2.7
        ret.steerRatio = 13.25   #Spec
        ret.steerRateCost = 0.4
      elif candidate == CAR.NEXO:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1885. + STD_CARGO_KG
        ret.wheelbase = 2.79
        ret.steerRatio = 12.5
      elif candidate == CAR.MOHAVE:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 2250. + STD_CARGO_KG
        ret.wheelbase = 2.895
        ret.steerRatio = 14.1
      elif candidate == CAR.I30:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1380. + STD_CARGO_KG
        ret.wheelbase = 2.65
        ret.steerRatio = 13.5
      elif candidate == CAR.AVANTE:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1275. + STD_CARGO_KG
        ret.wheelbase = 2.7
        ret.steerRatio = 13.5            # 14 is Stock | Settled Params Learner values are steerRatio: 15.401566348670535
      elif candidate == CAR.SELTOS:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1470. + STD_CARGO_KG
        ret.wheelbase = 2.63
        ret.steerRatio = 13.0
      elif candidate == CAR.PALISADE:
        ret.lateralTuning.init('lqr')
        ret.lateralTuning.lqr.scale = 1750.0
        ret.lateralTuning.lqr.ki = 0.03
        ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
        ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
        ret.lateralTuning.lqr.c = [1., 0.]
        ret.lateralTuning.lqr.k = [-100., 450.]
        ret.lateralTuning.lqr.l = [0.22, 0.318]
        ret.lateralTuning.lqr.dcGain = 0.003
        ret.mass = 1955. + STD_CARGO_KG
        ret.wheelbase = 2.90
        ret.steerRatio = 13.0


    # these cars require a special panda safety mode due to missing counters and checksums in the messages
    if candidate in [CAR.GENESIS, CAR.IONIQ_EV, CAR.IONIQ_HEV, CAR.KONA_EV]:
      ret.safetyModel = car.CarParams.SafetyModel.hyundaiLegacy

    ret.centerToFront = ret.wheelbase * 0.4

    # TODO: get actual value, for now starting with reasonable value for
    # civic and scaling by mass and wheelbase
    ret.rotationalInertia = scale_rot_inertia(ret.mass, ret.wheelbase)

    # TODO: start from empirically derived lateral slip stiffness for the civic and scale by
    # mass and CG position, so all cars will have approximately similar dyn behaviors
    ret.tireStiffnessFront, ret.tireStiffnessRear = scale_tire_stiffness(ret.mass, ret.wheelbase, ret.centerToFront,
                                                                         tire_stiffness_factor=tire_stiffness_factor)

    ret.enableCamera = is_ecu_disconnected(fingerprint[0], FINGERPRINTS, ECU_FINGERPRINT, candidate, Ecu.fwdCamera) or has_relay



    # ignore CAN2 address if L-CAN on the same BUS
    ret.mdpsBus = 1 if 593 in fingerprint[1] and 1296 not in fingerprint[1] else 0    # MDPS12
    ret.sasBus = 1 if 688 in fingerprint[1] and 1296 not in fingerprint[1] else 0     # SAS11
    ret.sccBus = 0 if 1056 in fingerprint[0] else 1 if 1056 in fingerprint[1] and 1296 not in fingerprint[1] else 2 if 1056 in fingerprint[2] else -1  # SCC11
    return ret

  def update(self, c, can_strings):
    self.cp.update_strings(can_strings)
    self.cp2.update_strings(can_strings)
    self.cp_cam.update_strings(can_strings)

    ret = self.CS.update(self.cp, self.cp2, self.cp_cam)
    ret.canValid = self.cp.can_valid and self.cp2.can_valid and self.cp_cam.can_valid

    # TODO: button presses
    buttonEvents = []
    if self.CS.cruise_buttons != self.CS.prev_cruise_buttons:
      be = car.CarState.ButtonEvent.new_message()
      be.type = ButtonType.unknown
      if self.CS.cruise_buttons != 0:
        be.pressed = True
        but = self.CS.cruise_buttons
      else:
        be.pressed = False
        but = self.CS.prev_cruise_buttons
      if but == Buttons.RES_ACCEL:
        be.type = ButtonType.accelCruise
      elif but == Buttons.SET_DECEL:
        be.type = ButtonType.decelCruise
      elif but == Buttons.CANCEL:
        be.type = ButtonType.cancel
      buttonEvents.append(be)
    if self.CS.cruise_main_button != self.CS.prev_cruise_main_button:
      be = car.CarState.ButtonEvent.new_message()
      be.type = ButtonType.altButton3
      be.pressed = bool(self.CS.cruise_main_button)
      buttonEvents.append(be)
    ret.buttonEvents = buttonEvents
    #ret.buttonEvents = []    

    events = self.create_common_events(ret)
    #TODO: addd abs(self.CS.angle_steers) > 90 to 'steerTempUnavailable' event

    if self.CC.lanechange_manual_timer:
      events.add(EventName.laneChangeManual)
    if self.CC.emergency_manual_timer:
      events.add(EventName.emgButtonManual)
    if self.CC.driver_steering_torque_above_timer:
      events.add(EventName.driverSteering)

    if self.CC.mode_change_timer and self.CS.out.cruiseState.modeSel == 0:
      events.add(EventName.modeChangeOpenpilot)
    elif self.CC.mode_change_timer and self.CS.out.cruiseState.modeSel == 1:
      events.add(EventName.modeChangeDistcurv)
    elif self.CC.mode_change_timer and self.CS.out.cruiseState.modeSel == 2:
      events.add(EventName.modeChangeDistance)
    elif self.CC.mode_change_timer and self.CS.out.cruiseState.modeSel == 3:
      events.add(EventName.modeChangeAutores)
    elif self.CC.mode_change_timer and self.CS.out.cruiseState.modeSel == 4:
      events.add(EventName.modeChangeStock)

    # low speed steer alert hysteresis logic (only for cars with steer cut off above 10 m/s)
    if ret.vEgo < (self.CP.minSteerSpeed + 2.) and self.CP.minSteerSpeed > 10.:
      self.low_speed_alert = True
    if ret.vEgo > (self.CP.minSteerSpeed + 4.):
      self.low_speed_alert = False
    if self.low_speed_alert:
      events.add(car.CarEvent.EventName.belowSteerSpeed)

    ret.events = events.to_msg()

    self.CS.out = ret.as_reader()
    return self.CS.out

  def apply(self, c, sm, CP ):
    can_sends = self.CC.update(c, self.CS, self.frame, sm, CP )

    self.frame += 1
    return can_sends
