from math import floor, frexp, ldexp

class Pdw():
    ''' PDW class structure '''

    NUM_BITS = {'pdw_format': 3, 'marked_operation': 2, 'frequency': 47,
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

    def convert_relative_power(self, relative_power):
        exponent_offset = -26
        num_mantissa_bits = 10
        num_exponent_bits = 5
        
        relative_power = 10**(relative_power/10)
        
        exponent = frexp(relative_power)[1]
        exponent = exponent - exponent_offset - 1
        
        if exponent >= 2**num_exponent_bits:
            self.relative_power = 0
            return self.relative_power
        
        if exponent >= 0:
            mantissa = ldexp(ldexp(
                       relative_power, 
                       -(exponent_offset + exponent)) - 1, 
                       num_mantissa_bits)
            mantissa = int(mantissa)
        else:
            self.relative_power = 0
            return self.relative_power
        
        self.relative_power = (exponent << num_mantissa_bits) + mantissa

        return self.relative_power

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

    # TODO: Needs work
    def read_csv(self):
        file_name = 'test.csv'
        with open(file_name) as file_object:
            lines = file_object.readlines()
            
        return lines

    def bin_field(self, value_dec, NUM_BITS):
        ''' This function takes a decimal integer value and converts it to a binary 
        string with a specified number of bits. The '0b' that is normally returned 
        with bin() is omitted.
        '''
        
        try:
            result = bin(value_dec)[2:].zfill(NUM_BITS)
        except Exception:
            raise
        else:
            return result

    def bin_word(self, field_list):
        ''' This function joins together all of the fields within a word to make a 
        single binary string.
        '''
        
        try:
            result = ''.join(field_list[::-1])
        except Exception:
            raise
        else:
            return result

    def byte_array(self, bin_word_str):
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
    
    def str2bin(self, byte_string):
        # return hex(int(byte_string, 2))
        return byte_string

    def word(self, *args):
        ''' This function takes in a variable number of 2-element list arguments,
        each representing fields within a pdw, and returns a list of byte strings.
        
        Keyword arguments:
        arg = [value, NUM_BITS]
        '''
        
        field_list = []
        
        try:
            for arg in args:
                arg_bin = self.bin_field(arg[0],arg[1])
                field_list.append(arg_bin)
                bin_word_str = self.bin_word(field_list)
            result = self.byte_array(bin_word_str)
            result = list(map(self.str2bin, result))
        except Exception:
            raise
        else:
            return result
            # file_name = 'test.pdw'
            # with open(file_name, 'wb') as file_object:
            #     file_object.write(bytearray(int(i, 16) for i in result))


pdw_test = Pdw(1,10**9,0,100000000,500000,0,'NONE',2,0,0,1,0,0,0)

word_bytes = pdw_test.word(
    [pdw_test.pdw_format,pdw_test.NUM_BITS['pdw_format']],
    [pdw_test.marked_operation,pdw_test.NUM_BITS['marked_operation']],
    [pdw_test.frequency,pdw_test.NUM_BITS['frequency']],
    [pdw_test.phase,pdw_test.NUM_BITS['phase']],
    [pdw_test.pulse_start_time,pdw_test.NUM_BITS['pulse_start_time']],
    [pdw_test.pulse_width,pdw_test.NUM_BITS['pulse_width']],
    [pdw_test.relative_power,pdw_test.NUM_BITS['relative_power']],
    [pdw_test.markers,pdw_test.NUM_BITS['markers']],
    [pdw_test.pulse_mode,pdw_test.NUM_BITS['pulse_mode']],
    [pdw_test.phase_control,pdw_test.NUM_BITS['phase_control']],
    [pdw_test.band_adjust,pdw_test.NUM_BITS['band_adjust']],
    [pdw_test.chirp_control,pdw_test.NUM_BITS['chirp_control']],
    [pdw_test.freq_phase_coding,pdw_test.NUM_BITS['freq_phase_coding']],
    [pdw_test.chirp_rate,pdw_test.NUM_BITS['chirp_rate']],
    [pdw_test.freq_band_map,pdw_test.NUM_BITS['freq_band_map']])


print(word_bytes)
