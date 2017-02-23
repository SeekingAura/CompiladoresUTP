# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Lexer

class CalcLexer(Lexer):
	fileName=""
	reserved_words = { 'BEGIN', 'CONST', 'END', 'IN', 'INOUT', 'MODULE', 'OUT', 'REG', 'TS', 'OC', 'TYPE', 'VAR', 'DIV', 'MOD', 'MUX', 'LATCH', 'SR', 'IF', 'THEN', 'ELSIF', 'FOR', 'DO', 'WHILE', 'RETURN' }
	
	tokens = {
		#valores
		'ID', 'INTEGER', 'LOGICVALUE'
		#simbolos
		'DOSPUNTOSIGUAL', 'MENORIGUAL', 'MAYORIGUAL', 'FLECHADERECHA', 'DOBLEPUNTO', "PLUS", "MENOS", "TIMES", "IQUAL", "POTENCIA", 
		#palabras reservadas
		*reserved_words,
	}
	ignore = ' \t'
	
	literals = { '~', '&', '|', '#', '<', '>', '(', ')', '[', ']', '{', '}', '.', ',', ';', ':' , "'", '!', '↑'}

	

	
	#Tokens - valores
	@_(r'[a-zA-Z_][a-zA-Z0-9_]*')
	def ID(self, t):
		#Control de palabras reservadas, o ma bien de priorizar check de expresión regular
		# Chec	k if name matches a reserved word (change token type if true)
		if t.value.upper() in self.reserved_words:
			t.type = t.value.upper()
		return t
	
	
	@_(r'\d+')#expresión regular que trabaja [0-9]
	def INTEGER(self, t):
		t.value = int(t.value)
		return t
	
	@_(r"'[0-1]")
	def LOGICVALUE(self, t):
		t.value = bool(int(t.value[1]))
		return t
		
	"""
	@_(r'\d+|[0-9a-fA-F]+H')
    def INTEGER(self, t):
        a=str(t.value)
        if(a[len(a)-1]== 'H'):#manejo hexa
            t.value = int (str(t.value), 16)
        else:
            t.value = int (str(t.value), 10)
        return t
	"""
	#Tokens - simbolos compuestos, operadores
	DOBLEPUNTO = r'\.\.'#r'[.][.]'
	FLECHADERECHA = r'->'
	MAYORIGUAL = r'>='
	MENORIGUAL = r'<='
	DOSPUNTOSIGUAL = r':='
	#Tokens - otros simbolos sencillos
	PLUS = r'\+'
	MINUS = r'-'
	TIMES = r'\*'
	IQUAL = r'='
	POTENCIA = r'\^'
	"""
	#forma de sobre-escribir token apartir de solo una expresión regular, puede estar sin definirse el token o en literales
	@_(r'\+')
	def PLUS(self, t):
		t.type = 'PLUS'      # Set token type to the expected literal
		return t
	"""
	#others ignore
	@_(r'\n+')
	def ignore_NEWLINE(self, t):
		self.lineno += t.value.count('\n')
	#r'\(\*([^*)]|\*[^*]\).*)*\*\)' expresion mejorada
	ignore_COMMENT=r'\(\*([^*]|\*[^)]|\))*\*\)'#\(\*[^*)\n]*\*\) sin saltos de linea, anterior \(\*[^*)]*\*\), 
	
	
	#error control
	@_(r'\(\*([^*]|\*[^)]|\))*')
	def error_COMMENT(self, t):
		print('File "{}" Line {} Colum {}'.format(self.fileName, t.lineno, self.getColumn(t)))
		print(t.value)
		print("ERROR - No terminó comentario")
		print("Se esperaba un *)")
	def error(self, value):
		print("Illegal character {}".format(value[0]))
		self.index += 1
		
	#metodos funcionales
	# Compute column.
	#     input is the input text string
	#     token is a token instance
	def getColumn(self, token):
		last_cr = self.text.rfind('\n', 0, token.index)+1
		#print("last_cr {}".format(last_cr))#verificando valor de indexados previos
		if last_cr < 0:
			last_cr = 0
		column = (token.index - last_cr) + 1
		return column
		
if __name__ == '__main__':
	import sys
	lexer = CalcLexer()
	if(len(sys.argv)!=2):#Verifica la cantidad de argumentos a la hora de compilar si no son 2. "py 'fichero.py' 'archivo'"
		sys.stderr.write('Usage: "{}" "filename"\n'.format(sys.argv[0]))#permite que al al compilar indique que debe de darse el archivo de la forma python.exe "fichero.py" "Archivo a abrir, como un simple print"
		raise SystemExit(1)#termina el programa
	file= open(sys.argv[1]).read()#en caso de que indique archivo tome el segundo string y abra el archivo y convierta con .read() a string
	maxLenthLine=0
	for linea in open(sys.argv[1]):
		if(maxLenthLine<len(linea)):
			maxLenthLine=len(linea)#verifica la columna maxima para el formato de centrado (visual en los print)
			print("malen",maxLenthLine)
	print("{:{align}{width}}".format("Archivo recibido - contenido inicio", align="^", width=maxLenthLine))
	print("-"*maxLenthLine)
	print(file)
	print("-"*maxLenthLine)
	print("{:{align}{width}}".format("Archivo recibido - contenido fin", align="^", width=maxLenthLine))
	
	#print("aplicando tokenize")
	lexer.fileName=sys.argv[1]
	for tok in lexer.tokenize(file):
		print("Linea {}, columna {}, indexado {}".format(tok.lineno, lexer.getColumn(tok), tok.index))
		print('tipo {} valor {}'.format(tok.type, tok.value))
