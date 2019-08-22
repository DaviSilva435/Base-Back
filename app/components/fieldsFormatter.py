class CpfFormatter:
    def clean(self, cpf):

        if not cpf.isdigit():
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")

        return cpf

def format(self, cpf):
    
    if cpf == "":
        return ""

    return "%s.%s.%s-%s" % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])

class CnpjFormatter:

    def clean(self, cnpj):

        if not cnpj.isdigit():
            cnpj = cnpj.replace("-", "")
            cnpj = cnpj.replace(".", "")
            cnpj = cnpj.replace("/", "")

        return cnpj

    def format(self, cnpj):
        
        if cnpj == "":
            return ""

        return "%s.%s.%s/%s-%s" % (cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14])

class CepFormatter:

    def clean(self, cep):

        if not cep.isdigit():
            cep = cep.replace("-", "")

        return cep

    def format(self, cep):

        if cep == "":
            return ""

        return "%s-%s" % (cep[0:5], cep[5:8])

class PhoneFormatter:

    def clean(self, phone):

        if not phone.isdigit():
            phone = phone.replace("-", "")
            phone = phone.replace("(", "")
            phone = phone.replace(")", "")
            phone = phone.replace(" ", "")

        return phone

    def format(self, phone):

        if phone == "":
            return ""

        return "(%s) %s-%s" % (phone[0:2], phone[2:7], phone[7:11])


class DateFormatter:

    def format(self, date):

        if date == None:
            return ""

        return date.strftime("%y-%m-%d")