#!/usr/bin/python

### VOLUME-APPLET ##############################################
# This is a collection of backends for volume-applet           #
# written by Mitchell Nemitz [mitchell . nemitz @ gmail . com] #
################################################################

import sys, os

class PulseAudio:
    boost = 3
    def __init__(self):
        try:
            import pa_interface
            self.pulse = pa_interface
        except:
            print "error : pa_interface : moduled failed to import\n"
            exit()
            
    def get_volume(self):
        sinks = self.pulse.get_all_s(is_sink=True)
        for s in sinks:
            if s[0] == "default": # Get default sink.
                val = s[1]        # Volume of left channel.
                val = val[:-1]    # Chop % sign.
                return float(val)/self.boost

    def set_volume(self, volume):
        volume = int(volume)*self.boost
        self.pulse.set_volume(str(volume)+"%")
    
    def get_mute(self):
        return self.pulse.get_s_mute(True, is_sink=True)
    
    def set_mute(self, mute):
        self.pulse.mute_s(True, is_sink=True)
    
    def get_boost(self):
        return True if self.boost!=1 else False

    def set_boost(self, level):
        self.boost = 3 if self.boost!=3 else 1
    
    def get_channels(self):
        return None  ### TODO

class PulseAudio2:
    boost = 3
    def __init__(self):
        try:
            import pa_interface
            self.pulse = pa_interface.Pulse()
        except:
            print "error : pa_interface : moduled failed to import\n"
            exit()
            
    def get_volume(self):
        sinks = self.pulse.get_sinks()
        for s in sinks:
            if s[0] == "default": # Get default sink.
                val = s[1]        # Volume of left channel.
                val = val[:-1]    # Chop % sign.
                return float(val)/self.boost

    def set_volume(self, volume):
        volume = int(volume)*self.boost
        self.pulse.set_volume(str(volume)+"%")
    
    def get_mute(self):
        return self.pulse.get_default_sink()[1]
    
    def set_mute(self, mute):
        self.pulse.mute()
    
    def get_boost(self):
        return True if self.boost!=1 else False

    def set_boost(self, level):
        self.boost = 3 if self.boost!=3 else 1
    
    def get_channels(self):
        return None  ### TODO

class ALSA:
    def __init__(self):
        try:
            import alsaaudio
            self.alsa = alsaaudio.Mixer('Master')
        except:
            print "error : alsaaudio : moduled failed to import\n"
            print "Debian: Install python-alsaaudio"
            print "Arch:   Install python-pyalsaaudio"
            exit()
    
    def get_volume(self):
        return self.alsa.getvolume()[0]
    
    def set_volume(self, volume):
        self.alsa.setvolume(int(volume))
    
    def get_mute(self):
        if self.alsa.getmute()[0] == 0: return False
        else: return True
    
    def set_mute(self, mute):
        if mute: self.alsa.setmute(1)
        else:    self.alsa.setmute(0)
        
    def get_channels(self):
        # This will eventually return a list of available channels for inclusion into
        # an integrated 'Audio Settings' dialog, when that happens no one really knows,
        # but it will be included in version 1.0 if we ever get there.
        pass
        
class OSS(object):
    def __init__(self):
        # Import whatever python module wraps your audio backend here, and
        # make sure the user knows if something went wrong.
        # A quick example:
        
        #try:
        #   import ossaudio as oss
        #except:
        #   print "error : ossaudio : moduled failed to import\n"
        #   print "Debian: Install python-ossaudio"
        #   print "Arch:   Install python-pyossaudio"
        #   exit()
        
        pass
    
    def get_volume(self):
        # Return the volume of the main channel as an int.
        
        #return alsa.Mixer('Master').getvolume()[0]
        
        pass
    
    def set_volume(self, volume):
        #Set the master channel volume to int(volume).
        
        #alsa.Mixer('Master').setvolume(int(volume))
        
        pass
    
    def get_mute(self):
        # The only complex thing you have to do here is check if
        # the channel is already muted. If it is, return true,
        # else return false.
        
        #if alsa.Mixer('Master').getmute()[0] == 0: return False
        #else: return True
        
        pass
    
    def set_mute(self, mute):
        # Again, check if they want to mute or unmute the volume,
        # then set the mute whichever way it goes. This is done
        # this way to prevent inverse toggling if you change the
        # mute somewhere else.
        
        #if mute: alsa.Mixer('Master').setmute(1)
        #else:    alsa.Mixer('Master').setmute(0)
        
        pass
        
    def get_channels(self):
        # This will eventually return a list of available channels for inclusion into
        # an integrated 'Audio Settings' dialog, when that happens no one really knows,
        # but it will be included in version 1.0 if we ever get there.
        pass

