# Embedded file name: /usr/lib/enigma2/python/Components/Converter/CamdRAED.py
from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll
import os

class AeonFHDCamdRAED(Poll, Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 2000
        self.poll_enabled = True

    @cached
    def getText(self):
        service = self.source.service
        info = service and service.info()
        camd = ''
        serlist = None
        camdlist = None
        nameemu = []
        nameser = []
        if not info:
            return ''
        elif fileExists('/etc/init.d/softcam') or fileExists('/etc/init.d/cardserver'):
            try:
                for line in open('/etc/init.d/softcam'):
                    if line.find('echo') > -1:
                        nameemu.append(line)

                camdlist = '%s' % nameemu[1].split('"')[1]
            except:
                pass

            try:
                for line in open('/etc/init.d/cardserver'):
                    if line.find('echo') > -1:
                        nameser.append(line)

                serlist = '%s' % nameser[1].split('"')[1]
            except:
                pass

            if serlist is None:
                serlist = ''
            elif camdlist is None:
                camdlist = ''
            elif serlist is None and camdlist is None:
                serlist = ''
                camdlist = ''
            return '%s %s' % (serlist, camdlist)
        else:
            if fileExists('/etc/startcam.sh'):
                try:
                    for line in open('/etc/startcam.sh'):
                        if line.find('script') > -1:
                            return '%s' % line.split('/')[-1].split()[0][:-3]

                except:
                    camdlist = None

            elif fileExists('/etc/CurrentDelCamName'):
                try:
                    camdlist = open('/etc/CurrentDelCamName', 'r')
                except:
                    return

            elif fileExists('/etc/BhFpConf'):
                try:
                    camdlist = open('/etc/BhCamConf', 'r')
                except:
                    return

            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/PKT/plugin.pyo'):
                if config.plugins.emuman.cam.value:
                    return config.plugins.emuman.cam.value
            elif fileExists('/usr/lib/enigma2/python/Plugins/newnigma2/eCamdCtrl/eCamdctrl.pyo'):
                from Plugins.newnigma2.eCamdCtrl.eCamdctrl import runningcamd
                if config.plugins.camdname.skin.value:
                    return runningcamd.getCamdCurrent()
            elif fileExists('/etc/.emustart') and fileExists('/etc/image-version'):
                try:
                    for line in open('/etc/.emustart'):
                        return line.split()[0].split('/')[-1]

                except:
                    return

            else:
                if fileExists('/etc/image-version') and not fileExists('/etc/.emustart'):
                    emu = ''
                    server = ''
                    for line in open('/etc/image-version'):
                        if '=AAF' in line or '=openATV' in line or '=opendroid' in line:
                            if config.softcam.actCam.value:
                                emu = config.softcam.actCam.value
                            if config.softcam.actCam2.value:
                                server = config.softcam.actCam2.value
                                if config.softcam.actCam2.value == 'no CAM 2 active':
                                    server = ''
                        elif '=vuplus' in line:
                            if fileExists('/tmp/.emu.info'):
                                for line in open('/tmp/.emu.info'):
                                    emu = line.strip('\n')

                        elif 'version=' in line and fileExists('/etc/CurrentBhCamName'):
                            emu = open('/etc/CurrentBhCamName').read()

                    return '%s %s' % (emu, server)
                if fileExists('/etc/active_emu.list'):
                    try:
                        camdlist = open('/etc/active_emu.list', 'r')
                    except:
                        return

                elif fileExists('/tmp/egami.inf', 'r'):
                    lines = open('/tmp/egami.inf', 'r').readlines()
                    for line in lines:
                        item = line.split(':', 1)
                        if item[0] == 'Current emulator':
                            return item[1].strip()

                else:
                    if fileExists('/tmp/ucm_cam.info'):
                        return open('/tmp/ucm_cam.info').read()
                    if fileExists('/tmp/cam.info'):
                        try:
                            camdlist = open('/tmp/cam.info', 'r')
                        except:
                            return

                    elif fileExists('/usr/bin/emuactive'):
                        try:
                            camdlist = open('/usr/bin/emuactive', 'r')
                        except:
                            return

                    elif fileExists('/etc/clist.list'):
                        try:
                            camdlist = open('/etc/clist.list', 'r')
                        except:
                            return

                    elif fileExists('/usr/lib/enigma2/python/Plugins/Bp/geminimain/lib/libgeminimain.so'):
                        try:
                            from Plugins.Bp.geminimain.plugin import GETCAMDLIST
                            from Plugins.Bp.geminimain.lib import libgeminimain
                            camdl = libgeminimain.getPyList(GETCAMDLIST)
                            cam = None
                            for x in camdl:
                                if x[1] == 1:
                                    cam = x[2]

                            return cam
                        except:
                            return

                    else:
                        return
            if serlist is not None:
                try:
                    cardserver = ''
                    for current in serlist.readlines():
                        cardserver = current

                    serlist.close()
                except:
                    pass

            else:
                cardserver = 'NA'
            if camdlist is not None:
                try:
                    emu = ''
                    for current in camdlist.readlines():
                        emu = current

                    camdlist.close()
                except:
                    pass

            else:
                emu = 'NA'
            return '%s %s' % (cardserver.split('\n')[0], emu.split('\n')[0])

    text = property(getText)

    def changed(self, what):
        Converter.changed(self, what)