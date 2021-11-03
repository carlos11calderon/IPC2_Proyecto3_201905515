class DocumentoTE: 

    def __init__(self, tiempo, referencia, nitE, nitR, Valor, iva, total, ErrorNitE, ErrorNitR, ErrorIva, ErrorTotal, esCorrecta):
        self.tiempo=tiempo
        self.referencia = referencia
        self.nitE = nitE
        self.nitR = nitR
        self.valor = Valor
        self.iva = iva
        self.total =total
        self.ErrorNitE = ErrorNitE
        self.ErrorNitR = ErrorNitR
        self.ErrorIva= ErrorIva
        self.ErrorTotal = ErrorTotal
        self.Correcta = esCorrecta
        self.Revisada = False
        