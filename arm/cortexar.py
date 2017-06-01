# BSP support for Cortex-A/R
from build_rts_support.bsp import BSP
from build_rts_support.target import DFBBTarget


class CortexARArch(BSP):
    @property
    def name(self):
        return "cortex-ar"

    def __init__(self):
        super(CortexARArch, self).__init__()
        self.add_sources('arch', [
            'arm/src/i-arm_v7ar.ads',
            'arm/src/i-arm_v7ar.adb',
            'src/i-cache/i-cache.ads',
            'src/i-cache/armv7/i-cache.adb'])
        self.add_sources('gnarl', [
            'src/s-bbcpsp/arm/s-bbcpsp.ads',
            'src/s-bbcppr/old/s-bbcppr.ads',
            'src/s-bbcppr/arm/s-bbcppr.adb',
            'src/s-bbinte/generic/s-bbinte.adb'])


class CortexARTarget(DFBBTarget):
    @property
    def target(self):
        return 'arm-eabi'

    @property
    def parent(self):
        return CortexARArch

    @property
    def has_newlib(self):
        return True

    @property
    def zfp_system_ads(self):
        return 'system-xi-arm.ads'


class Rpi2(CortexARTarget):
    @property
    def name(self):
        return "rpi2"

    @property
    def loaders(self):
        return ('RAM', )

    @property
    def mcu(self):
        return 'cortex-a7'

    @property
    def fpu(self):
        return 'vfpv4'

    @property
    def has_timer_64(self):
        return True

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mhard-float',
                '-mcpu=%s' % self.mcu,
                '-mfpu=%s' % self.fpu,
                '-marm', '-mno-unaligned-access')

    @property
    def readme_file(self):
        return 'arm/rpi2/README'

    @property
    def sfp_system_ads(self):
        return 'system-xi-arm-sfp.ads'

    @property
    def full_system_ads(self):
        return 'system-xi-arm-full.ads'

    def __init__(self):
        super(Rpi2, self).__init__(
            mem_routines=True,
            small_mem=False)

        self.add_linker_script('arm/rpi2/ram.ld', loader='RAM')
        self.add_sources('crt0', [
            'arm/rpi2/i-raspberry_pi.ads',
            'arm/rpi2/start-ram.S',
            'arm/rpi2/memmap.s',
            'src/s-textio/rpi2-mini/s-textio.adb',
            'src/s-macres/rpi2/s-macres.adb'])
        self.add_sources('gnarl', [
            'arm/rpi2/a-intnam.ads',
            'src/s-bbpara/rpi2/s-bbpara.ads',
            'src/s-bbbosu/rpi2/s-bbbosu.adb'])


class TMS570(CortexARTarget):
    @property
    def name(self):
        return "tms570"

    @property
    def loaders(self):
        return ('PROBE', 'FLASH', 'MONITOR', 'HIRAM', 'LORAM')

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mbig-endian', '-mhard-float', '-mcpu=cortex-r4',
                '-mfpu=vfpv3-d16', '-marm')

    @property
    def readme_file(self):
        return 'arm/tms570/README'

    @property
    def sfp_system_ads(self):
        return 'system-xi-arm-sfp.ads'

    @property
    def full_system_ads(self):
        return 'system-xi-arm-full.ads'

    def __init__(self):
        super(TMS570, self).__init__(
            mem_routines=True,
            small_mem=True)

        self.add_linker_script('arm/tms570/common.ld')
        self.add_linker_script('arm/tms570/tms570.ld', loader='PROBE')
        self.add_linker_script('arm/tms570/flash.ld', loader='FLASH')
        self.add_linker_script('arm/tms570/monitor.ld', loader='MONITOR')
        self.add_linker_script('arm/tms570/hiram.ld', loader='HIRAM')
        self.add_linker_script('arm/tms570/loram.ld', loader='LORAM')
        self.add_linker_switch('-Wl,-z,max-page-size=0x1000',
                               loader=['FLASH', 'MONITOR', 'HIRAM', 'LORAM'])

        self.add_sources('crt0', [
            'arm/tms570/sys_startup.S',
            'arm/tms570/crt0.S',
            'arm/tms570/start-ram.S',
            'arm/tms570/start-rom.S',
            'src/s-textio/tms570/s-textio.adb',
            'src/s-macres/tms570/s-macres.adb'])
        self.add_sources('gnarl', [
            'src/a-intnam/tms570/a-intnam.ads',
            'src/s-bbpara/tms570/s-bbpara.ads',
            'src/s-bbbosu/tms570/s-bbbosu.adb',
            'src/s-bbsumu/generic/s-bbsumu.adb'])


class Zynq7000(CortexARTarget):
    @property
    def name(self):
        return "zynq7000"

    @property
    def loaders(self):
        return ('RAM', )

    @property
    def mcu(self):
        return 'cortex-a9'

    @property
    def fpu(self):
        return 'vfpv3'

    @property
    def has_timer_64(self):
        return True

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mhard-float',
                '-mcpu=%s' % self.mcu,
                '-mfpu=%s' % self.fpu,
                '-marm', '-mno-unaligned-access')

    @property
    def readme_file(self):
        return 'arm/zynq/README'

    @property
    def sfp_system_ads(self):
        return 'system-xi-cortexa-sfp.ads'

    @property
    def full_system_ads(self):
        return 'system-xi-cortexa-full.ads'

    def __init__(self):
        super(Zynq7000, self).__init__(
            mem_routines=True,
            small_mem=False)
        self.add_linker_script('arm/zynq/ram.ld', loader='RAM')
        self.add_sources('crt0', [
            'arm/zynq/start-ram.S',
            'arm/zynq/memmap.inc',
            'src/s-textio/zynq/s-textio.adb',
            'src/s-macres/zynq/s-macres.adb'])
        self.add_sources('gnarl', [
            'src/a-intnam/zynq/a-intnam.ads',
            'src/s-bbpara/cortexa9/s-bbpara.ads',
            'src/s-bbbosu/cortexa9/s-bbbosu.adb'])
