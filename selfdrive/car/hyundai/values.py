# flake8: noqa

from cereal import car
from selfdrive.car import dbc_dict
from common.params import Params
from selfdrive.kyd_conf import kyd_conf

Ecu = car.CarParams.Ecu

# Steer torque limits
class SteerLimitParams:
  kyd = kyd_conf()
  STEER_MAX = int(kyd.conf['steerMax'])   # 409 is the max, 255 is stock
  STEER_DELTA_UP = int(kyd.conf['steerDeltaUp'])  # 3
  STEER_DELTA_DOWN = int(kyd.conf['steerDeltaDown'])  # 7
  STEER_DRIVER_ALLOWANCE = 50
  STEER_DRIVER_MULTIPLIER = 2
  STEER_DRIVER_FACTOR = 1


class CAR:
  AVANTE = "HYUNDAI AVANTE"
  SONATA = "HYUNDAI SONATA"
  SONATA_HEV = "HYUNDAI SONATA Hybrid"
  SONATA_TURBO = "HYUNDAI SONATA Turbo"
  GRANDEUR = "HYUNDAI GRANDEUR"
  GRANDEUR_HEV = "HYUNDAI GRANDEUR Hybrid"
  GENESIS = "GENESIS"
  SANTAFE = "HYUNDAI SANTAFE"
  KONA = "HYUNDAI KONA"
  KONA_HEV = "HYUNDAI KONA Hybrid"
  KONA_EV = "HYUNDAI KONA ELECTRIC"
  IONIQ_HEV = "HYUNDAI IONIQ HYBRID"
  IONIQ_EV = "HYUNDAI IONIQ ELECTRIC"
  K5 = "KIA K5"
  K5_HEV = "KIA K5 Hybrid"
  K7 = "KIA K7"
  K7_HEV = "KIA K7 Hybrid"
  STINGER = "KIA STINGER"
  SORENTO = "KIA SORENTO"
  NIRO_HEV = "KIA NIRO Hybrid"
  NIRO_EV = "KIA NIRO ELECTRIC"
  NEXO = "HYUNDAI NEXO"
  MOHAVE = "KIA MOHAVE"
  I30 = "HYUNDAI I30"
  SELTOS = "KIA SELTOS"
  PALISADE = "HYUNDAI PALISADE"


class Buttons:
  NONE = 0
  RES_ACCEL = 1
  SET_DECEL = 2
  GAP_DIST = 3
  CANCEL = 4

params = Params()
fingerprint_issued_fix = params.get("FingerprintIssuedFix", encoding='utf8') == "1"

if fingerprint_issued_fix:
  FINGERPRINTS = { 
  }
else:
  FINGERPRINTS = {
    CAR.KONA_HEV: [{
      68: 8, 127: 8, 304: 8, 320: 8, 339: 8, 352: 8, 356: 4, 544: 8, 576: 8, 593: 8, 688: 5, 832: 8, 881: 8, 882: 8, 897: 8, 902: 8, 903: 8, 905: 8, 909: 8, 916: 8, 1040: 8, 1042: 8, 1056: 8, 1057: 8, 1078: 4, 1136: 6, 1138: 4, 1151: 6, 1155: 8, 1157: 4, 1164: 8, 1168: 7, 1173: 8, 1183: 8, 1186: 2, 1191: 2, 1193: 8, 1225: 8, 1265: 4, 1280: 1, 1287: 4, 1290: 8, 1291: 8, 1292: 8, 1294: 8, 1312: 8, 1322: 8, 1342: 6, 1345: 8, 1348: 8, 1355: 8, 1363: 8, 1369: 8, 1378: 8, 1379: 8, 1407: 8, 1419: 8, 1427: 6, 1429: 8, 1430: 8, 1448: 8, 1456: 4, 1470: 8, 1476: 8, 1535: 8
      }]
    }


ECU_FINGERPRINT = {
  Ecu.fwdCamera: [832, 1156, 1191, 1342]
}

CHECKSUM = {
  "crc8": [CAR.SANTAFE, CAR.SONATA, CAR.PALISADE],
  "6B": [CAR.SORENTO, CAR.GENESIS],
}

FEATURES = {
  # which message has the gear
  "use_cluster_gears": [],     # Use Cluster for Gear Selection, rather than Transmission
  "use_tcu_gears": [],                                    # Use TCU Message for Gear Selection
  "use_elect_gears": [CAR.KONA_HEV], # Use TCU Message for Gear Selection
  "send_lfa_mfa": [],
  # these cars use the FCA11 message for the AEB and FCW signals, all others use SCC12
  "use_fca": [],

  "use_bsm": [CAR.KONA_HEV],
}

EV_HYBRID = [CAR.KONA_HEV, CAR.K5_HEV, CAR.SONATA_HEV, CAR.GRANDEUR_HEV, CAR.IONIQ_HEV, CAR.IONIQ_EV, CAR.NIRO_HEV, CAR.KONA_EV, CAR.NIRO_EV, CAR.NEXO]

DBC = {
  CAR.AVANTE: dbc_dict('hyundai_kia_generic', None),
  CAR.SONATA: dbc_dict('hyundai_kia_generic', None),
  CAR.SONATA_HEV: dbc_dict('hyundai_kia_generic', None),
  CAR.SONATA_TURBO: dbc_dict('hyundai_kia_generic', None),
  CAR.GRANDEUR: dbc_dict('hyundai_kia_generic', None),
  CAR.GRANDEUR_HEV: dbc_dict('hyundai_kia_generic', None),
  CAR.GENESIS: dbc_dict('hyundai_kia_generic', None),
  CAR.SANTAFE: dbc_dict('hyundai_kia_generic', None),
  CAR.KONA: dbc_dict('hyundai_kia_generic', None),
  CAR.KONA_HEV: dbc_dict('hyundai_kia_generic', None),
  CAR.KONA_EV: dbc_dict('hyundai_kia_generic', None),
  CAR.IONIQ_HEV: dbc_dict('hyundai_kia_generic', None),
  CAR.IONIQ_EV: dbc_dict('hyundai_kia_generic', None),
  CAR.K5: dbc_dict('hyundai_kia_generic', None),
  CAR.K5_HEV: dbc_dict('hyundai_kia_generic', None),
  CAR.K7: dbc_dict('hyundai_kia_generic', None),
  CAR.K7_HEV: dbc_dict('hyundai_kia_generic', None),
  CAR.STINGER: dbc_dict('hyundai_kia_generic', None),
  CAR.NIRO_HEV: dbc_dict('hyundai_kia_generic', None),
  CAR.NIRO_EV: dbc_dict('hyundai_kia_generic', None),
  CAR.NEXO: dbc_dict('hyundai_kia_generic', None),
  CAR.MOHAVE: dbc_dict('hyundai_kia_generic', None),
  CAR.I30: dbc_dict('hyundai_kia_generic', None),
  CAR.SELTOS: dbc_dict('hyundai_kia_generic', None),
  CAR.PALISADE: dbc_dict('hyundai_kia_generic', None),
  CAR.SORENTO: dbc_dict('hyundai_kia_generic', None),
}


STEER_THRESHOLD = 80
