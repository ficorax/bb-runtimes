from build_rts_support.bsp import BSP
from arm.cortexm import CortexMArch, CortexMTarget


class SamCommonBSP(BSP):
    @property
    def name(self):
        return 'sam'

    @property
    def parent(self):
        return CortexMArch

    @property
    def loaders(self):
        return ('ROM', 'SAMBA', 'USER')

    def __init__(self):
        super(SamCommonBSP, self).__init__()

        self.add_linker_script('arm/sam/common-SAMBA.ld', loader='SAMBA')
        self.add_linker_script('arm/sam/common-ROM.ld', loader='ROM')

        self.add_sources('crt0', [
            's-sam4s.ads',
            'arm/sam/start-rom.S',
            'arm/sam/start-ram.S',
            'arm/sam/setup_pll.ads'])
        self.add_sources('gnarl', {
            's-bbpara.ads': 's-bbpara-sam4s.ads'})


class SamGenericBSP(BSP):
    @property
    def parent(self):
        return SamCommonBSP

    @property
    def has_single_precision_fpu(self):
        assert False, "Not implemented"

    @property
    def compiler_switches(self):
        base = ('-mlittle-endian', '-mthumb', '-mcpu=cortex-m4')

        if not self.has_single_precision_fpu:
            return base
        else:
            return base + ('-mhard-float', '-mfpu=fpv4-sp-d16', )

    def __init__(self):
        super(SamGenericBSP, self).__init__()

        self.add_linker_script(
            'arm/sam/%s/memory-map.ld' % self.name,
            loader=('SAMBA', 'ROM'))
        self.add_sources('crt0', [
            'arm/sam/%s/board_config.ads' % self.name,
            'arm/sam/%s/setup_pll.adb' % self.name,
            'arm/sam/%s/svd/i-sam.ads' % self.name,
            'arm/sam/%s/svd/i-sam-efc.ads' % self.name,
            'arm/sam/%s/svd/i-sam-pmc.ads' % self.name,
            'arm/sam/%s/svd/i-sam-sysc.ads' % self.name,
            {'s-textio.adb': 's-textio-sam4s.adb'}])
        # FIXME: s-textio.adb is invalid for the g55

        # ravenscar support
        self.add_sources('gnarl', [
            'arm/sam/%s/svd/handler.S' % self.name,
            'arm/sam/%s/s-bbbopa.ads' % self.name,
            'arm/sam/%s/s-bbmcpa.ads' % self.name,
            {'a-intnam.ads': 'arm/sam/%s/svd/a-intnam.ads' % self.name}])


class Sam4sBSP(SamGenericBSP):
    @property
    def name(self):
        return 'sam4s'

    @property
    def has_single_precision_fpu(self):
        return False


class SamG55BSP(SamGenericBSP):
    @property
    def name(self):
        return 'samg55'

    @property
    def has_single_precision_fpu(self):
        return True


class Sam(CortexMTarget):
    @property
    def bspclass(self):
        if self.board == 'sam4s':
            return Sam4sBSP
        elif self.board == 'samg55':
            return SamG55BSP
        else:
            assert False, "Unexpected board %s" % self.board

    @property
    def has_single_precision_fpu(self):
        return self.bsp.has_single_precision_fpu

    def __init__(self, board):
        self.board = board
        super(Sam, self).__init__()