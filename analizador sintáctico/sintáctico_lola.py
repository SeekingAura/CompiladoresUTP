# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Parser
from léxico_lola import CalcLexer

class CalcParser(Parser):
	debugfile='parser.out'#control de depuración
	
	tokens = tokens = CalcLexer.tokens
	
	'''
	tipoSimple : tipoBasico
		|	ID conjuntoExpresiones
		;
	'''
	
	@_('tipoBasico',
		'ID conjuntoExpresiones')
	def tipoSimple(self, p):
		pass
		
	'''
	tipoBasico : 'BIT'
		| 'TS'
		| 'OC'
		;
	'''
	@_('BIT', 'TS', 'OC')
	def tipoBasico(self, p):
		pass
	
	'''
	conjuntoExpresiones :
	|	'(' listaExpresiones ')'
	;
	'''
	
	@_('empty', '( listaExpresiones )')
	conjuntoExpresiones(self, p):
		pass
		
	'''
	listaExpresiones : expresion expresionComa
		;
	'''
	
	@_('expresion expresionComa')
	def listaExpresiones(self, p):
		pass
		
	'''
	expresionComa :  expresionComa
	|	',' expresion
	;
	'''
	@_('expresionComa', ', expresion'):
	def expresionComa(self, p):
		pass
		
	'''
	tipo : expresionCorchete tipoSimple
	;
	'''
	@_('expresionCorchete tipoSimple')
	def tipo(self, p)
		pass
		
	'''
	expresionCorchete : expresionCorchete
	|	'[' expresion ']'
	;
	'''
	@_('expresionCorchete', '[ expresion ]')
	def expresionCorchete(self, p):
		pass
		
	'''
	declaracionConstante : ID ':=' expresion ';'
	;
	'''
	
	@_('ID DOSPUNTOSIGUAL expresion')
	def declaracionConstante()
		pass
		
	'''
	declaracionVariable : listaId ':' tipo ';'
	;
	'''
	@_('listaId DOSPUNTOS tipo PUNTOYCOMA')
	def declaracionVariable(self, p):
		pass
		
	'''
	listaId : ID identificadorComa
		;
	'''
	@_('ID identificadorComa')
	def listaId(self, p):
		pass
		
	'''
	IDComa : IDComa
	|	',' ID
	'''
	@_('IDComa', 'COMA ID')
	def IDComa(self, p):
		pass
	
	'''
	selector : selector
	|	IDComa
	|	enteroPunto
	|	expresionCorchete
	;
	'''
	@_('selector')
	
	"""
	program: program statement
			| statment
			;
	"""
	
	@_('program statement',
		'statment')
	def program(self, p):
		pass
		
		
		
	@_('error')
	def program(self, p):
		pass
		
if __name__ == '__main__':
	import sys
	lexer = CalcLexer()
	parser = CalcParser()
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
	result = parser.parse(file)
