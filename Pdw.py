from math import floor

class Pdw():
    ''' Class structure for individual PDWs '''

    num_bits = {'pdw_format': 3, 'marked_operation': 2, 'frequency': 47,
                'phase': 12, 'pulse_start_time': 64, 'pulse_width': 32,
                'relative_power': 15, 'markers': 12, 'pulse_mode': 2,
                'phase_control': 1, 'band_adjust': 2, 'chirp_control': 3,
                'freq_phase_coding': 9, 'chirp_rate': 17, 'freq_band_map': 3}

    def __init__(self, marked_operation, frequency, phase, 
                 pulse_start_time, pulse_width, relative_power, markers,
                 pulse_mode, phase_control, band_adjust, chirp_control,
                 freq_phase_coding, chirp_rate, freq_band_map, pdw_format = 1):
        self.pdw_format = pdw_format
        self.marked_operation = marked_operation
        self.convert_frequency(frequency)
        self.convert_phase(phase)
        self.pulse_start_time = pulse_start_time
        self.pulse_width = pulse_width
        self.convert_relative_power(relative_power)
        self.convert_markers(markers)
        self.pulse_mode = pulse_mode
        self.phase_control = phase_control
        self.band_adjust = band_adjust
        self.chirp_control = chirp_control
        self.freq_phase_coding = freq_phase_coding
        self.convert_chirp_rate(chirp_rate)
        self.freq_band_map = freq_band_map

    def convert_frequency(self, frequency):
        self.frequency =  floor(frequency * 1024 + 0.5)

    def convert_phase(self, phase):
        self.phase = floor((phase*2**12)/360 + 0.5)

    # TODO: add convert_relative_power()
    def convert_relative_power(self, relative_power):
        self.relative_power = relative_power

    def convert_markers(self, markers):
        valid_markers = set('123456789ABC')

        marker_dict = {'1': 1, '2': 2, '3': 4, '4': 8, '5': 16, '6': 32, '7': 64, 
                       '8': 128, '9': 256, 'A': 512, 'B': 1024, 'C': 2048}

        if markers.upper() == 'ALL':
            selected_markers = set('123456789ABC')
        elif markers.upper() == 'NONE':
            selected_markers = set('')
        else:
            selected_markers = set(markers.upper())

        marker_set = valid_markers & selected_markers

        marker_value = 0

        for marker in marker_dict.keys():
            if marker in marker_set:
                marker_value += marker_dict[marker]

        self.markers = marker_value

    # TODO: Add convert_chirp_rate()
    def convert_chirp_rate(self, chirp_rate):
        self.chirp_rate = chirp_rate

    # TODO: add read_csv()
    def read_csv(self):
        pass

    def bin_field(value_dec, num_bits):
        ''' This function takes a decimal integer value and converts it to a binary 
        string with a specified number of bits. The '0b' that is normally returned 
        with bin() is omitted.
        '''
        try:
            result = bin(value_dec)[2:].zfill(num_bits)
        except Exception:
            raise
        else:
            return result

    def bin_word(field_list):
        ''' This function joins together all of the fields within a word to make a 
        single binary string.
        '''
        try:
            result = ''.join(field_list[::-1])
        except Exception:
            raise
        else:
            return result

    def byte_array(bin_word_str):
        ''' This function breaks a binary word string up into a list of bytes. '''
        byte = ''
        result = []

        try:
            for idx, bit in enumerate(bin_word_str):
                byte = byte + bit
                if idx % 8 == 7:
                    result.append(byte) # append byte to list
                    byte = ''
        except Exception:
            raise
        else:
            return result

    def word(*args):
        ''' This function takes in a variable number of 2-element list arguments,
        each representing fields within a pdw, and returns a list of byte strings.

        Keyword arguments:
        arg = [value, num_bits]
        '''
        field_list = []

        try:
            for arg in args:
                arg_bin = bin_field(arg[0],arg[1])
                field_list.append(arg_bin)
                bin_word_str = bin_word(field_list)
            result = byte_array(bin_word_str)
        except Exception:
            raise
        else:
            return result

    word_bytes = word(
        [self.pdw_format,num_bits['pdw_format']],
        [self.marked_operation,num_bits['marked_operation']],
        [self.frequency,num_bits['frequency']],
        [self.phase,num_bits['phase']],
        [self.pulse_start_time,num_bits['pulse_start_time']],
        [self.pulse_width,num_bits['pulse_width']],
        [self.relative_power,num_bits['relative_power']],
        [self.markers,num_bits['markers']],
        [self.pulse_mode,num_bits['pulse_mode']],
        [self.phase_control,num_bits['phase_control']],
        [self.band_adjust,num_bits['band_adjust']],
        [self.chirp_control,num_bits['chirp_control']],
        [self.freq_phase_coding,num_bits['freq_phase_coding']],
        [self.chirp_rate,num_bits['chirp_rate']],
        [self.freq_band_map,num_bits['freq_band_map']])


#pdw_test = Pdw(1,10**9,0,100000000,500000,26624,'NONE',2,0,0,1,0,0,0)
