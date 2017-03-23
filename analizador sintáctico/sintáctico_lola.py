from sly import Parser
from léxico_lola import CalcLexer
#from ast_lola import *
class CalcParser(Parser):
	debugfile='parser.out'#control de depuración
	#precedence = (
    #   ('left', '+', '-'),            # Unary minus operator
    #)
	tokens = CalcLexer.tokens
	
	def __init__(self):
		self.error=0
		
	'''
	lola : lola module
	| module
	;
	'''
	@_('lola modulo')
	def lola(self, p):
		pass
		#p.lola.append(p.modulo)
		#return p.lola
	
	@_('modulo')
	def lola(self, p):
		pass
		#return Lola([p.modulo])
			
	'''
	tipoSimple : tipoBasico
		|	ID "(" listaExpresiones ")"
		|	ID
		;
	'''
	@_('tipoBasico') 
	def tipoSimple(self, p):
		pass
		#return TipoSimple(p.tipoBasico)
	
	@_('ID "(" listaExpresiones ")"', 'ID')
	def tipoSimple(self, p):
		pass
		#return TipoSimpleID(p.ID, p.conjuntoExpresiones)
		
	'''
	tipoBasico : 'BIT'
		| 'TS'
		| 'OC'
		;
	'''
	@_('BIT', 
	'TS', 
	'OC')
	def tipoBasico(self, p):
		pass
		#return p
		
	'''
	listaExpresiones : listaExpresiones "," expresion
		| expresion
		;
	'''
	@_('listaExpresiones "," expresion')
	def listaExpresiones(self, p):
		pass
		#ListaExpresiones(p.expresion, p.expresionComa)

	@_('expresion')
	def listaExpresiones(self, p):
		pass
		#return ExpresionComa(p.expresionComaR)
		
	'''
	tipo : "[" expresion "]" tipo
		|	tipoSimple
		;
	'''
	@_('"[" expresion "]" tipo', 'tipoSimple')
	def tipo(self, p):
		pass
		#return Tipo(p.expresionCorchete, p.tipoSimple)
	
	'''
	declaracionConstante : ID DOSPUNTOSIGUAL expresion ";"'
	;
	'''
	@_('ID DOSPUNTOSIGUAL expresion ";"')
	def declaracionConstante(self, p):
		pass
		#return DeclaracionConstante(p.ID, p.expresion)
	
	'''
	declaracionVariable : listaId ":" tipo ";"
	;
	'''
	@_('listaId ":" tipo ";"')
	def declaracionVariable(self, p):
		pass
		#return DeclaracionVariable(p.listaId, p.tipo)
	
	'''
	listaId : listaId "," ID
		|	ID
		;
	'''
	@_('ID', 'listaId "," ID')
	def listaId(self, p):
		pass
		#return ListaId(p.ID, p.IDComa)
	
	'''
	selector : selectorR
	|	empty
	;
	'''
	
	@_('selectorR', 
	'empty')
	def selector(self, p):
		pass
	
	'''
	selectoR : selectorR selectorRR
	|	selectorRR
	;
	'''
	@_('selectorR selectorRR',
	'selectorRR')
	def selectorR(self, p):
		pass
		
	'''
	selectorRR : "." ID
	|	"." INTEGER
	|	"[" expresion "]"
	;
	'''
	@_('"." ID',
	'"." INTEGER',
	'"[" expresion "]"')
	def selectorRR(self, p):
		pass
		
	'''
	factor : ID selector
	|	valorLogico
	|	INTEGER
	|	"~" factor
	|	"?" factor
	|	'FLECHAARRIBA factor'
	|	"(" expresion ")"
	|	"MUX" "(" expresion ":" expresion "," expresion ")"
	|	"MUX" "(" expresion "," expresion ":" expresion "," expresion "," expresion "," expresion)
	|	"REG" "(" expresion ")"
	|	"REG" "(" expresion "," expresion ")"
	|	"LATCH" "(" expresion "," expresion ")"
	|	"SR" "(" expresion "," expresion ")"
	;
	'''
	#'"↑" factor', genera error de enconding
	@_('ID selector', 
	'LOGICVALUE', 
	'INTEGER', 
	'FLECHAARRIBA factor',
	'"~" factor', 
	'"(" expresion ")"', 
	'MUX "(" expresion ":" expresion "," expresion ")"', 
	'MUX "(" expresion "," expresion ":" expresion "," expresion "," expresion "," expresion ")"',
	'REG "(" expresion ")"',
	'REG "(" expresion "," expresion ")"',
	'LATCH "(" expresion "," expresion ")"', 
	'SR "(" expresion , expresion ")"')
	def factor(self, p):
		pass
		#cuando se tiene tokens del mismo en lo largo de la gramatica, se puede referir con p.expresion0, p.expresion1
	
	'''
	termino : termino simbolosProd factor
	|	factor
	;
	'''	
	@_('termino simbolosProd factor', 'factor')
	def termino(self, p):
		pass
		
	
	'''
	simbolosProd : "*"
	|	SLASH
	|	"DIV"
	|	"MOD"
	;
	'''
	@_('"*"',
	'"/"',
	'DIV',
	'MOD')
	def simbolosProd(self, p):
		pass
		
	'''
	expresion : expresion "+" termino
	|	expresion "-" termino
	|	termino
	;
	'''
	@_('expresion "+" termino',
	'expresion "-" termino',
	'termino')
	def expresion(self, p):
		pass
		
	'''
	asignacion : ID selector DOSPUNTOSIGUAL expresion
	|	ID selector DOSPUNTOSIGUAL condicion "|" expresion
	;
	'''
	@_('ID selector DOSPUNTOSIGUAL expresion',
	'ID selector DOSPUNTOSIGUAL condicion "|" expresion')
	def asignacion(self, p):
		pass
	
	'''
	condicion : expresion
	;
	'''
	@_('expresion')
	def condicion(self, p):
		pass
	
	'''
	relacion : expresion "=" expresion
	|	expresion "#" expresion
	|	expresion "<" expresion
	|	expresion MENORIGUAL expresion
	|	expresion ">" expresion
	|	expresion MAYORIGUAL expresion
	;
	'''
	@_('expresion "=" expresion',
	'expresion "#" expresion',
	'expresion "<" expresion',
	'expresion MENORIGUAL expresion',
	'expresion ">" expresion',
	'expresion MAYORIGUAL expresion')
	def relacion(self, p):
		pass
		
	'''
	sentenciaSi : "IF" relacion "THEN" sentenciaSecuencia sentenciaSiSino sentenciaSiEntonces "END"
	;
	'''
	@_('IF relacion THEN sentenciaSecuencia sentenciaSiSino sentenciaSiEntonces END')
	def sentenciaSi(self, p):
		pass
		
	'''
	sentenciaSiSino : sentenciaSiSinoR
	|	empty
	;
	'''
	@_('sentenciaSiSinoR',
	'empty')
	def sentenciaSiSino(self, p):
		pass
	
	'''
	sentenciaSiSinoR : sentenciaSiSinoR "ELSIF" relacion "THEN" sentenciaSecuencia
	|	"ELSIF" relacion "THEN" sentenciaSecuencia
	;
	'''
	
	@_('sentenciaSiSinoR ELSIF relacion THEN sentenciaSecuencia',
	'ELSIF relacion THEN sentenciaSecuencia')
	def sentenciaSiSinoR(self, p):
		pass

	'''
	sentenciaSiEntonces : "ELSE" sentenciaSecuencia
	|	empty
	;
	'''
	@_('ELSE sentenciaSecuencia',
	'empty')
	def sentenciaSiEntonces(self, p):
		pass
		
	'''
	sentenciaPara : "FOR" ID ":=" expresion DOBLEPUNTO expresion "DO" sentenciaSecuencia "END"
	;
	'''
	@_('FOR ID DOSPUNTOSIGUAL expresion DOBLEPUNTO expresion DO sentenciaSecuencia END')
	def sentenciaPara(self, p):
		pass
		
	'''
	sentencia : asignacion
	|	asignacionUnidad
	|	sentenciaSi
	|	sentenciaPara
	|	empty
	;
	'''
	@_('asignacion', 
	'asignacionUnidad', 
	'sentenciaSi', 
	'sentenciaPara',
	'empty')
	def sentencia(self, p):
		pass
	
	'''
	sentenciaSecuencia : sentenciaSecuencia ";" sentencia
	|	sentencia
	;
	'''
	@_('sentenciaSecuencia ";" sentencia', 'sentencia')
	def sentenciaSecuencia(self, p):
		pass

	'''
	modulo : "MODULE" ID ";"
	declaracionTipoPuntoComa
	declaracionConstanteCONST
	declaracionVariableIN
	declaracionVariableINOUT
	declaracionVariableOUT
	declaracionVariableVAR
	sentenciaSecuenciaBEGIN
	END ID "."
	;
	'''
	@_('MODULE ID ";" declaracionTipoPuntoComa declaracionConstanteCONST declaracionVariableIN declaracionVariableINOUT declaracionVariableOUT declaracionVariableVAR sentenciaSecuenciaBEGIN END ID "."')
	def modulo(self, p):
		pass
		#return Modulo(p.declaracionTipoPuntoComa, p.declaracionConstanteCONST, p.declaracionVariableIN, p.declaracionVariableINOUT, p.declaracionVariableOUT, p.declaracionVariableVAR, p.sentenciaSecuenciaBEGIN, p.ID)
		
	'''
	declaracionTipoPuntoComa : declaracionTipoPuntoComaR
	|	empty
	;
	'''	
	@_('declaracionTipoPuntoComaR',
	'empty')
	def declaracionTipoPuntoComa(self, p):
		pass
	
	'''
	declaracionTipoPuntoComaR : declaracionTipoPuntoComaR declaracionTipo ";"
	|	declaracionTipo ";"
	;
	'''
	@_('declaracionTipoPuntoComaR declaracionTipo ";"',
	'declaracionTipo ";"')
	def declaracionTipoPuntoComaR(self, p):
		pass

	'''
	declaracionConstanteCONST : "CONST" declaracionConstanteRecursivo
	|	empty
	;
	'''
	@_('CONST declaracionConstanteRecursivo',
	'empty')
	def declaracionConstanteCONST(self, p):
		pass
		
	'''
	declaracionConstanteRecursivo : declaracionConstanteRecursivoR
	|	empty
	;
	'''
	@_('declaracionConstanteRecursivoR',
	'empty')
	def declaracionConstanteRecursivo(self, p):
		pass
	
	'''
	declaracionConstanteRecursivoR : declaracionConstanteRecursivoR declaracionConstante
	|	declaracionConstante
	;
	'''
	@_('declaracionConstanteRecursivoR declaracionConstante',
	'declaracionConstante')
	def declaracionConstanteRecursivoR(self, p):
		pass
		
	'''
	declaracionVariableIN : "IN" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('IN declaracionVariableRecursivo',
	'empty')
	def declaracionVariableIN(self, p):
		pass
	
	'''
	declaracionVariableRecursivo : declaracionVariableRecursivoR
	|	empty
	;
	'''
	@_('declaracionVariableRecursivoR',
	'empty')
	def declaracionVariableRecursivo(self, p):
		pass
	
	'''
	declaracionVariableRecursivoR : declaracionVariableRecursivoR declaracionVariable
	|	declaracionVariable
	;
	'''
	@_('declaracionVariableRecursivoR declaracionVariable',
	'declaracionVariable')
	def declaracionVariableRecursivoR(self, p):
		pass
	
	'''
	declaracionVariableINOUT : "INOUT" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('INOUT declaracionVariableRecursivo',
	'empty')
	def declaracionVariableINOUT(self, p):
		pass
		
	'''
	declaracionVariableOUT : "OUT" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('OUT declaracionVariableRecursivo',
	'empty')
	def declaracionVariableOUT(self, p):
		pass
	
	'''
	declaracionVariableVAR : "VAR" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('VAR declaracionVariableRecursivo', 
	'empty')
	def declaracionVariableVAR(self, p):
		pass
		
	'''
	sentenciaSecuenciaBEGIN : "BEGIN" sentenciaSecuencia
	|	empty
	;
	'''
	@_('BEGIN sentenciaSecuencia', 
	'empty')
	def sentenciaSecuenciaBEGIN(self, p):
		pass

	'''
	tipoFormal : expresionCorcheteO "BIT"
	;
	'''
	@_('expresionCorcheteO BIT')
	def tipoFormal(self, p):
		pass
		
	'''
	expresionCorcheteO : expresionCorcheteOR
	|	empty
	;
	'''
	@_('expresionCorcheteOR',
	'empty')
	def expresionCorcheteO(self, p):
		pass
	
	'''
	expresionCorcheteOR : expresionCorcheteOR "[" expresionOpcional "]"
	|	"[" expresionOpcional "]"
	;
	'''
	@_('expresionCorcheteOR "[" expresionOpcional "]"',
	'"[" expresionOpcional "]"')
	def expresionCorcheteOR(self, p):
		pass
	
	'''
	expresionOpcional : expresion
	|	empty
	;
	'''
	@_('expresion',
	'empty')
	def expresionOpcional(self, p):
		pass
		
	'''
	tipoFormalBus : expresionCorcheteO "TS"
	|	expresionCorcheteO "OC"
	;
	'''
	@_('expresionCorcheteO TS', 
	'expresionCorcheteO OC')
	def tipoFormalBus(self, p):
		pass
		
	'''
	declaracionTipo : "TYPE" ID simboloPor listaIdParentesis ";" 
	declaracionConstanteCONST 
	tipoFormalIN
	tipoFormlINOUT
	declaracionVariableOUT 
	declaracionVariableVAR 
	sentenciaSecuenciaBEGIN 
	END ID
	;
	'''
	@_('TYPE ID simboloPor listaIdParentesis ";" declaracionConstanteCONST tipoFormalIN tipoFormlINOUT declaracionVariableOUT declaracionVariableVAR sentenciaSecuenciaBEGIN END ID')
	def declaracionTipo(self, p):
		pass
		
	'''
	simboloPor : "*"
	|	empty
	;
	'''
	@_('"*"',
	'empty')
	def simboloPor(self, p):
		pass
		
	'''
	listaIdParentesis : "(" listaId ")"
	|	empty
	;
	'''
	@_('"(" listaId ")"',
	'empty')
	def listaIdParentesis(self, p):
		pass
		
	'''
	tipoFormalIN : IN tipoFormallistaId
	|	empty
	;
	'''
	@_('IN tipoFormallistaId',
	'empty')
	def tipoFormalIN(self, p):
		pass
		
	'''
	tipoFormallistaId : tipoFormallistaIdR 
	|	empty
	;
	'''
	@_('tipoFormallistaIdR',
	'empty')
	def tipoFormallistaId(self, p):
		pass
		
	'''
	tipoFormallistaIdR : tipoFormallistaIdR listaId ":" tipoFormal ";"
	|	listaId ":" tipoFormal ";"
	;
	'''
	@_('tipoFormallistaIdR listaId ":" tipoFormal ";"',
	'listaId ":" tipoFormal ";"')
	def tipoFormallistaIdR(self, p):
		pass

	'''
	tipoFormnalINOUT : INOUT tipoFormlBuslistaId
	|	empty
	;
	'''
	@_('INOUT tipoFormlBuslistaId',
	'empty')
	def tipoFormlINOUT(self, p):
		pass
		
	'''
	tipoFormlBuslistaId : tipoFormlBuslistaIdR
	|	empty
	;
	'''
	@_('tipoFormlBuslistaIdR',
	'empty')
	def tipoFormlBuslistaId(self, p):
		pass
	
	'''
	tipoFormlBuslistaIdR : tipoFormlBuslistaIdR listaId ":" tipoFormalBus ";"
	|	listaId ":" tipoFormalBus ";"
	;
	'''
	@_('tipoFormlBuslistaIdR listaId ":" tipoFormalBus ";"',
	'listaId ":" tipoFormalBus ";"')
	def tipoFormlBuslistaIdR(self, p):
		pass

	'''
	assinacionUnidad : ID selector "(" listaExpresiones ")"
	'''
	@_('ID selector "(" listaExpresiones ")"')
	def asignacionUnidad(self, p):
		pass
	#prueba de errores
	"""
	@_('ID selector error listaExpresiones ")"')
	def asignacionUnidad(self, p):
		print ("ERROR 14 - ( expected")
		self.error+=1
		return "fatal"
	"""
	
	'''
	empty :
	'''
	@_('')
	def empty(self, p):
		pass
	
	
def parse(data, debug=0):
	p = parser.parse(lexer.tokenize(data))
	if parser.error:
		return None
	return p
		
if __name__ == '__main__':
	import sys
	lexer = CalcLexer()
	parser = CalcParser()
	if(len(sys.argv)!=2):#Verifica la cantidad de argumentos a la hora de compilar si no son 2. "py 'fichero.py' 'archivo'"
		sys.stderr.write('Usage: "{}" "filename"\n'.format(sys.argv[0]))#permite que al al compilar indique que debe de darse el archivo de la forma python.exe "fichero.py" "Archivo a abrir, como un simple print"
		raise SystemExit(1)#termina el programa
	file= open(sys.argv[1]).read()#en caso de que indique archivo tome el segundo string y abra el archivo y convierta con .read() a string
	"""
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
	"""
	#print("aplicando tokenize")
	lexer.fileName=sys.argv[1]
	parse(file)