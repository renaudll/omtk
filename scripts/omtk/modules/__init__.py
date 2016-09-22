# Import body modules
import rigRibbon
import rigSplineIK
import rigFK
import rigIK
import rigLimb
import rigTwistbone
import rigLeg
import rigArm
import rigDpSpine
import rigHand
import rigHead
import rigNeck
# Import face modules
import rigFaceAvar
import rigFaceAvarGrps
import rigFaceBrow
import rigFaceLids
import rigFaceLips
import rigFaceSquint
import rigFaceJaw
import rigFaceEyes
import rigFaceNose


def _reload():
    # Reload body modules
    reload(rigFK)
    reload(rigIK)
    reload(rigRibbon)
    reload(rigSplineIK)
    reload(rigTwistbone)
    reload(rigLimb)
    reload(rigArm)
    reload(rigLeg)
    reload(rigHand)
    reload(rigDpSpine)
    reload(rigNeck)
    reload(rigHead)

    # Reload face modules
    reload(rigFaceAvar)
    reload(rigFaceAvarGrps)
    reload(rigFaceBrow)
    reload(rigFaceLids)
    reload(rigFaceLips)
    reload(rigFaceSquint)
    reload(rigFaceJaw)
    reload(rigFaceEyes)
    reload(rigFaceNose)
