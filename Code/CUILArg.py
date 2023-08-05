class CUIL:
    def __init__(self, Dni, Sexo):
        self.dni = Dni.replace('.', '')
        self.sexo = Sexo
        self.cuil = ''
        self.get_dni()
        self.get_sexo()
        self.get_cuil()

    def get_dni(self):
        if len(self.dni) == 7:
            self.dni = '0' + self.dni
            return True
        elif len(self.dni) != 8:
            return False

    def get_sexo(self):
        if self.sexo.startswith('f'):
            self.sexo = 'f'
        elif self.sexo.startswith('m'):
            self.sexo = 'm'
        else:
            return False
        return True

    def get_cuil(self):
        self.cuil = ''

        if self.sexo == 'f':
            self.cuil += '27'
        else:
            self.cuil += '20'
        self.cuil += '-'
        self.cuil += self.dni

        Suma_digitos = str(11 - (int(self.cuil[0]) * 5 + int(self.cuil[1]) * 4 + int(self.cuil[3]) * 3 + int(self.cuil[4]) * 2 +
                                int(self.cuil[5]) * 7 + int(self.cuil[6]) * 6 + int(self.cuil[7]) * 5 +
                                int(self.cuil[8]) * 4 + int(self.cuil[9]) * 3 + int(self.cuil[10]) * 2) % 11)

        if Suma_digitos == '11':
            Suma_digitos = '0'
        elif Suma_digitos == '10':
            if self.sexo == 'f':
                self.cuil = '23' + self.cuil[2:]
                Suma_digitos = '4'
            else:
                self.cuil = '23' + self.cuil[2:]
                Suma_digitos = '9'

        self.cuil += '-'
        self.cuil += Suma_digitos

    def get_first_two_numbers(self):
        return self.cuil[:2]

    def get_dni_number(self):
        return self.cuil[3:-2]

    def get_last_digit(self):
        return self.cuil[-1]


def get(Dni, Sexo):
    cuil_instance = CUIL(Dni=Dni, Sexo=Sexo)
    return cuil_instance.cuil, cuil_instance.get_first_two_numbers(), cuil_instance.get_dni_number(), cuil_instance.get_last_digit()

