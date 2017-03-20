from sly import Parser
from léxico_lola import CalcLexer
#from ast_lola import *
class CalcParser(Parser):
	debugfile='parser.out'#control de depuración
	precedence = (
        ('left', '+', '-'),            # Unary minus operator
    )
	tokens = CalcLexer.tokens
	
	def __init__(self):
		self.error=0
		
	"""	
	lola : lola module
	| module
	;
	"""
	@_('lola modulo')
	def lola(self, p):
		pass
		#p.lola.append(p.modulo)
		#return lola
	
	@_('modulo')
	def lola(self, p):
		pass
		#return Lola([p.modulo])
	
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
	tipoSimple : tipoBasico
		|	ID conjuntoExpresiones
		;
	'''
	@_('tipoBasico') 
	def tipoSimple(self, p):
		pass
		#return TipoSimple(p.tipoBasico)
	@_('ID conjuntoExpresiones')
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
	conjuntoExpresiones : '(' listaExpresiones ')'
	|	
	;
	'''
	@_('empty')
	def conjuntoExpresiones(self, p):
		pass
	
	@_('"(" listaExpresiones ")"')
	def conjuntoExpresiones(self, p):
		pass
		#return ConjuntoExpresiones(p.listaExpresiones)
		
	'''
	listaExpresiones : expresion expresionComa
		;
	'''
	@_('expresion expresionComa')
	def listaExpresiones(self, p):
		pass
		#ListaExpresiones(p.expresion, p.expresionComa)
	'''
	expresionComa :  expresionComaR 
	|
	;
	'''

	@_('expresionComaR')
	def expresionComa(self, p):
		pass
		#return ExpresionComa(p.expresionComaR)
	
	@_('empty')
	def expresionComa(self, p):
		pass
		#return None
	
	'''
	expresionComaR : expresionComaR "," expresion
	|	"," expresion
	;
	'''
	
	@_('expresionComaR "," expresion')
	def expresionComaR(self, p):
		pass
		#p.expresionComaR.append(p.expresion)
		#return p.expresionComaR
	
	@_('"," expresion')
	def expresionComaR(self, p):
		pass
		#return ExpresionComaR([p.expresion])
		
	'''
	tipo : expresionCorchete tipoSimple
	;
	'''
	@_('expresionCorchete tipoSimple')
	def tipo(self, p):
		pass
		#return Tipo(p.expresionCorchete, p.tipoSimple)
	'''
	expresionCorchete : expresionCorcheteR
	|
	;
	'''
	@_('expresionCorcheteR')
	def expresionCorchete(self, p):
		pass
		#return ExpresionCorchete(p.expresionCorchete)
	
	@_('empty')
	def expresionCorchete(self, p):
		pass
		#return None
	
	'''
	expresionCorcheteR : expresionCorcheteR "[" expresion "]"
	|	"[" expresion "]"
	;
	'''
	@_('expresionCorcheteR "[" expresion "]"')
	def expresionCorcheteR(self, p):
		pass
		#p.expresionCorcheteR.append(p.expresion)
		#p.expresionCorcheteR
	
	@_('"[" expresion "]"')
	def expresionCorcheteR(self, p):
		pass
		#return ExpresionCorcheteR([p.expresion])
	'''
	declaracionConstante : ID ":=" expresion ";"'
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
	listaId : ID IDComa
		;
	'''
	@_('ID IDComa')
	def listaId(self, p):
		pass
		#return ListaId(p.ID, p.IDComa)
		
	'''
	IDComa : IDComaR
	|
	;
	'''

	@_('IDComaR',
	'empty')
	def IDComa(self, p):
		pass
	
	'''
	IDComaR : IDComaR "," ID
	|	"," ID
	;
	'''
	@_('IDComaR "," ID',
	'"," ID')
	def IDComaR(self, p):
		pass
	'''
	selector : selectorR
	|
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
	|	"(" expresion ")"
	|	"MUX" "(" expresion ":" expresion "," expresion ")"
	|	"MUX" "(" expresion "," expresion ":" expresion "," expresion "," expresion "," expresion)
	|	"REG" "(" expresionComaO expresion ")"
	|	"LATCH" "(" expresion "," expresion ")"
	|	"SR" "(" expresion "," expresion ")"
	;
	'''
	#'"↑" factor', genera error de enconding
	@_('ID selector', 
	'LOGICVALUE', 
	'INTEGER', 
	'"~" factor', 
	'"(" expresion ")"', 
	'MUX "(" expresion ":" expresion "," expresion ")"', 
	'MUX "(" expresion "," expresion ":" expresion "," expresion "," expresion "," expresion ")"', 
	'REG "(" expresionComaO expresion', 
	'LATCH "(" expresion "," expresion ")"', 
	'SR "(" expresion , expresion ")"')
	def factor(self, p):
		pass
		#cuando se tiene tokens del mismo en lo largo de la gramatica, se puede referir con p.expresion0, p.expresion1
		
	'''
	expresionComaO : expresion ","
	|	
	;
	'''
	@_('expresion ","',
	'empty')
	def expresionComaO(self, p):
		pass
		
	'''
	termino : factor terminoOperadores
	;
	'''	
	@_('factor terminoOperadores')
	def termino(self, p):
		pass
		
	'''
	terminoOperadores : terminoOperadoresR 
	|
	;
	'''
	@_('terminoOperadoresR', 
	'empty')
	def terminoOperadores(self, p):
		pass
	
	'''
	terminoOperadoresR : terminoOperadoresR simbolosProd factor
	|	simbolosProd factor
	;
	'''
	@_('terminoOperadoresR simbolosProd factor',
	'simbolosProd factor')
	def terminoOperadoresR(self, p):
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
	expresion : termino terminoMasMenos
	;
	'''
	@_('termino terminoMasMenos')
	def expresion(self, p):
		pass
		
	'''
	terminoMasMenos : terminoMasMenosR
	|
	;
	'''
	@_('terminoMasMenosR',
	'empty')
	def terminoMasMenos(self, p):
		pass
	
	'''
	terminoMasMenosR : terminoMasMenosR simbolosMasMenos termino
	|	simbolosMasMenos termino
	;
	'''
	@_('terminoMasMenosR simbolosMasMenos termino',
	'simbolosMasMenos termino')
	def terminoMasMenosR(self, p):
		pass
	
	'''
	simbolosMasMenos : "+"
	|	"-"
	;
	'''
	@_('"+"', 
	'"-"')
	def simbolosMasMenos(self, p):
		pass
		
	'''
	asignacion : ID selector DOSPUNTOSIGUAL condicionOr expresion
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
	relacion : expresion simbolosRelacion expresion
	;
	'''
	@_('expresion simbolosRelacion expresion')
	def relacion(self, p):
		pass
		
	'''
	simbolosRelacion : "="
	|	"#"
	|	"<"
	|	"<="
	|	">"
	|	">="
	;
	'''
	@_('"="', 
	'"#"', 
	'"<"', 
	'MENORIGUAL', 
	'">"', 
	'MAYORIGUAL')
	def simbolosRelacion(self, p):
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
	|
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
	|
	;
	'''
	@_('ELSE sentenciaSecuencia',
	'empty')
	def sentenciaSiEntonces(self, p):
		pass
		
	'''
	sentenciaPara : "FOR" ID ":=" expresion ".." expresion "DO" sentenciaSecuencia "END"
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
	|
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
	sentenciaSecuencia : sentencia sentenciaPuntoComa
	;
	'''
	@_('sentencia sentenciaPuntoComa')
	def sentenciaSecuencia(self, p):
		pass
		
	'''
	sentenciaPuntoComa : sentenciaPuntoComaR
	|
	;
	'''
	@_('sentenciaPuntoComaR', 
	'empty')
	def sentenciaPuntoComa(self, p):
		pass
	
	'''
	sentenciaPuntoComaR : sentenciaPuntoComaR ";" sentencia
	|	";" sentencia
	;
	'''
	@_('sentenciaPuntoComaR ";" sentencia',
	'";" sentencia')
	def sentenciaPuntoComaR(self, p):
		pass

	
		
	'''
	declaracionTipoPuntoComa : declaracionTipoPuntoComaR
	|
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
	|	
	;
	'''
	@_('CONST declaracionConstanteRecursivo',
	'empty')
	def declaracionConstanteCONST(self, p):
		pass
		
	'''
	declaracionConstanteRecursivo : declaracionConstanteRecursivoR
	|
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
	|	
	;
	'''
	@_('IN declaracionVariableRecursivo',
	'empty')
	def declaracionVariableIN(self, p):
		pass
		
	'''
	declaracionVariableINOUT : "INOUT" declaracionVariableRecursivo
	|	
	;
	'''
	@_('INOUT declaracionVariableRecursivo',
	'empty')
	def declaracionVariableINOUT(self, p):
		pass
		
	'''
	declaracionVariableOUT : "OUT" declaracionVariableRecursivo
	|	
	;
	'''
	@_('OUT declaracionVariableRecursivo',
	'empty')
	def declaracionVariableOUT(self, p):
		pass
	
	'''
	declaracionVariableVAR : "VAR" declaracionVariableRecursivo
	|	
	;
	'''
	@_('VAR declaracionVariableRecursivo', 
	'empty')
	def declaracionVariableVAR(self, p):
		pass
		
	'''
	sentenciaSecuenciaBEGIN : "BEGIN" sentenciaSecuencia
	|	
	;
	'''
	@_('BEGIN sentenciaSecuencia', 
	'empty')
	def sentenciaSecuenciaBEGIN(self, p):
		pass
		
	'''
	declaracionVariableRecursivo : declaracionVariableRecursivoR
	|
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
	tipoFormal : expresionCorcheteO "BIT"
	;
	'''
	@_('expresionCorcheteO BIT')
	def tipoFormal(self, p):
		pass
		
	'''
	expresionCorcheteO : expresionCorcheteOR
	|
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
	|	
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
	|	
	;
	'''
	@_('"*"',
	'empty')
	def simboloPor(self, p):
		pass
		
	'''
	listaIdParentesis : "(" listaId ")"
	|	
	;
	'''
	@_('"(" listaId ")"',
	'empty')
	def listaIdParentesis(self, p):
		pass
		
	'''
	tipoFormalIN : IN tipoFormallistaId
	|	
	;
	'''
	@_('IN tipoFormallistaId',
	'empty')
	def tipoFormalIN(self, p):
		pass
		
	'''
	tipoFormallistaId : tipoFormallistaIdR 
	|
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
	|	
	;
	'''
	@_('INOUT tipoFormlBuslistaId',
	'empty')
	def tipoFormlINOUT(self, p):
		pass
		
	'''
	tipoFormlBuslistaId : tipoFormlBuslistaIdR
	|
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
	
	@_('ID selector error listaExpresiones ")"')
	def asignacionUnidad(self, p):
		print ("ERROR 14 - ( expected")
		self.error+=1
		return "fatal"
	
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