import time


class VerticeInvalidoException(Exception):
    pass


class ArestaInvalidaException(Exception):
    pass


class Grafo:
    QTDE_MAX_SEPARADOR = 1
    SEPARADOR_ARESTA = '-'

    def __init__(self, N=[], A={}):
        '''
        Constrói um objeto do tipo Grafo. Se nenhum parâmetro for passado, cria um Grafo vazio.
        Se houver alguma aresta ou algum vértice inválido, uma exceção é lançada.
        :param N: Uma lista dos vértices (ou nodos) do grafo.
        :param V: Uma dicionário que guarda as arestas do grafo. A chave representa o nome da aresta e o valor é uma string que contém dois vértices separados por um traço.
        '''
        for v in N:
            if not (Grafo.verticeValido(v)):
                raise VerticeInvalidoException('O vértice ' + v + ' é inválido')

        self.N = N

        # for a in A:
        #     if not (self.arestaValida(A[a])):
        #         raise ArestaInvalidaException('A aresta ' + A[a] + ' é inválida')

        self.A = A

    def arestaValida(self, aresta=''):
        '''
        Verifica se uma aresta passada como parâmetro está dentro do padrão estabelecido.
        Uma aresta é representada por um string com o formato a-b, onde:
        a é um substring de aresta que é o nome de um vértice adjacente à aresta.
        - é um caractere separador. Uma aresta só pode ter um único caractere como esse.
        b é um substring de aresta que é o nome do outro vértice adjacente à aresta.
        Além disso, uma aresta só é válida se conectar dois vértices existentes no grafo.
        :param aresta: A aresta que se quer verificar se está no formato correto.
        :return: Um valor booleano que indica se a aresta está no formato correto.
        '''

        # Não pode haver mais de um caractere separador
        if aresta.count(Grafo.SEPARADOR_ARESTA) != Grafo.QTDE_MAX_SEPARADOR:
            return False

        # Índice do elemento separador
        i_traco = aresta.index(Grafo.SEPARADOR_ARESTA)

        # O caractere separador não pode ser o primeiro ou o último caractere da aresta
        if i_traco == 0 or aresta[-1] == Grafo.SEPARADOR_ARESTA:
            return False

        # Verifica se as arestas antes de depois do elemento separador existem no Grafo
        if not (self.existeVertice(aresta[:i_traco])) or not (self.existeVertice(aresta[i_traco + 1:])):
            return False

        return True

    @classmethod
    def verticeValido(self, vertice=''):
        '''
        Verifica se um vértice passado como parâmetro está dentro do padrão estabelecido.
        Um vértice é um string qualquer que não pode ser vazio e nem conter o caractere separador.
        :param vertice: Um string que representa o vértice a ser analisado.
        :return: Um valor booleano que indica se o vértice está no formato correto.
        '''
        return vertice != '' and vertice.count(Grafo.SEPARADOR_ARESTA) == 0

    def existeVertice(self, vertice=''):
        '''
        Verifica se um vértice passado como parâmetro pertence ao grafo.
        :param vertice: O vértice que deve ser verificado.
        :return: Um valor booleano que indica se o vértice existe no grafo.
        '''
        return Grafo.verticeValido(vertice) and self.N.count(vertice) > 0

    def existeAresta(self, aresta=''):
        '''
        Verifica se uma aresta passada como parâmetro pertence ao grafo.
        :param aresta: A aresta a ser verificada
        :return: Um valor booleano que indica se a aresta existe no grafo.
        '''
        existe = False
        if Grafo.arestaValida(self, aresta):
            for k in self.A:
                if aresta == self.A[k]:
                    existe = True

        return existe

    def adicionaVertice(self, v):
        '''
        Adiciona um vértice no Grafo caso o vértice seja válido e não exista outro vértice com o mesmo nome
        :param v: O vértice a ser adicionado
        :raises: VerticeInvalidoException se o vértice passado como parâmetro não puder ser adicionado
        '''
        if self.verticeValido(v) and not self.existeVertice(v):
            self.N.append(v)
        else:
            raise VerticeInvalidoException('O vértice ' + v + ' é inválido')

    def adicionaAresta(self, nome, a):
        '''
        Adiciona uma aresta no Grafo caso a aresta seja válida e não exista outra aresta com o mesmo nome
        :param v: A aresta a ser adicionada
        :raises: ArestaInvalidaException se a aresta passada como parâmetro não puder ser adicionada
        '''
        if self.arestaValida(a):
            self.A[nome] = a
        else:
            ArestaInvalidaException('A aresta ' + self.A[a] + ' é inválida')

    def vertices_nao_adjacentes(self):
        arestas = self.A.values()
        resultado = []

        for i in self.N:
            for j in self.N:
                aresta_indo = "{}{}{}".format(i, self.SEPARADOR_ARESTA, j)
                aresta_voltando = "{}{}{}".format(j, self.SEPARADOR_ARESTA, i)
                if aresta_indo not in arestas and aresta_voltando not in arestas:
                    resultado.append(aresta_indo)
        return resultado

    def ha_laco(self):
        arestas = self.A.values()
        for i in arestas:
            v1, v2 = i.split(self.SEPARADOR_ARESTA)
            if v1 == v2:
                return True
        return False

    def ha_paralelas(self):
        arestas = list(self.A.values())

        for i in arestas:
            v1, v2 = i.split(self.SEPARADOR_ARESTA)
            if (arestas.count("{}{}{}".format(v1, self.SEPARADOR_ARESTA, v2)) > 1):
                return True

        return False

    def grau(self, vertice):
        aresta = self.A

        cont = 0
        for i in aresta:
            V1, V2 = aresta[i].split(self.SEPARADOR_ARESTA)
            if V1 == vertice or V2 == vertice:
                cont += 1

        return cont

    def arestas_sobre_vertice(self, vertice):
        aresta = self.A

        arestas_final = []
        for i in aresta:
            V1, V2 = aresta[i].split(self.SEPARADOR_ARESTA)
            if V1 == vertice or V2 == vertice:
                arestas_final.append(i)
        return arestas_final

    def eh_completo(self):
        arestas = list(self.A.values())

        verticies = self.N

        lista_completo = []

        if len(verticies) == 1:
            return True
        elif len(verticies) == 2:
            return True

        for i in range(len(verticies)):
            for j in range(i + 1, len(verticies)):
                lista_completo.append("{}{}{}".format(verticies[i], self.SEPARADOR_ARESTA, verticies[j]))

        if len(lista_completo) != len(arestas):
            return False
        else:
            for i in range(len(lista_completo)):
                v1, v2 = lista_completo[i].split("-")
                if (lista_completo[i] not in arestas):
                    if "{}{}{}".format(v2, self.SEPARADOR_ARESTA, v1) not in arestas:
                        return False
                    continue

            return True

    def DFS(self, verticie, visitados):

        visitados.append(verticie)
        for a in self.A:
            v1, v2 = self.A[a].split(self.SEPARADOR_ARESTA)
            if v2 not in visitados and v1 == verticie:
                visitados.append(a)
                self.DFS(v2, visitados)
        return visitados


    def ha_ciclo(self):

        arestas = self.A
        vertices = self.N
        vertices_da_arestas = list(arestas.values())
        # print(arestas)

        # print(vertices_da_arestas)

        for i in range(len(vertices)):

            possivel_ciclo = []
            if (self.grau(vertices[i]) > 1):
                verticiesPertencentes, arestasPertencentes = self.arestas_e_vertices_pertencentes(vertices[i], '',
                                                                                                  possivel_ciclo)

                atual = len(possivel_ciclo)
                for j in range(len(verticiesPertencentes)):
                    for k in range(1, len(verticiesPertencentes)):
                        self.analisar_caminho(vertices[i], verticiesPertencentes[j], verticiesPertencentes[k],
                                              possivel_ciclo)
                        if (len(set(possivel_ciclo)) > atual):
                            return possivel_ciclo
                        else:
                            possivel_ciclo = []

        return False


    def arestas_e_vertices_pertencentes(self, x, raiz, possivel_ciclo):
        listaVertices = []
        arestas = self.A
        dicaArestas = {}

        for i in arestas:
            # print(i)
            # print(arestas[i])

            v1, v2 = arestas[i].split(self.SEPARADOR_ARESTA)
            if v1 == x and v2 != raiz:
                possivel_ciclo.append(x + self.SEPARADOR_ARESTA + v2)
                listaVertices.append(v2)
                dicaArestas[str(i)] = x + self.SEPARADOR_ARESTA + v2
            elif v2 == x and v1 != raiz:
                possivel_ciclo.append(v1 + self.SEPARADOR_ARESTA + x)
                listaVertices.append(v1)
                dicaArestas[str(i)] = v1 + self.SEPARADOR_ARESTA + x

        # print(listaVertices)
        # print(dicaArestas)

        return listaVertices, dicaArestas

    def analisar_caminho(self, raiz, inicio, fim, lista):

        arestas = self.A.values()
        possivel_aresta = inicio + self.SEPARADOR_ARESTA + fim

        if possivel_aresta in arestas:
            lista.append(possivel_aresta)
        else:
            self.arestas_e_vertices_pertencentes(fim, inicio, lista)



    def caminho(self,n):

        n = n + 1
        passados = []
        verticies = self.N
        for i in verticies:
            passados.append(i)
            self.vertices_pertencentes(i, passados)

            if len(passados) > n:
                subtrair = len(passados)- n
                for j in range(subtrair):
                    passados.pop()
                    return " - ".join(passados)
            elif len(passados) == n:
                return " - ".join(passados)
            passados = []


        return False


    def vertices_pertencentes(self, x, lista_passados):
        listaVertices = []
        arestas = self.A


        for i in arestas:
            v1, v2 = arestas[i].split(self.SEPARADOR_ARESTA)
            if v1 == x and v2 not in lista_passados:
                lista_passados.append(v2)
                self.vertices_pertencentes(v2, lista_passados)

            elif v2 == x and v1 not in lista_passados:
                lista_passados.append(v1)
                self.vertices_pertencentes(v1, lista_passados)



    def conexo(self):

        vertices = self.N
        inicial = vertices[0]

        for x in range(1, len(vertices)):
            l = []
            if self.caminho_dois_vertices(inicial, vertices[x], l) == False:
                return False

        return True


    def caminho_dois_vertices(self, x, y, analizados):

        analizados.append(x)
        arestas = self.A.values()
        a = x + self.SEPARADOR_ARESTA + y
        if a in arestas or a[::-1] in arestas:
            return True

        if self.grau(x) == 0 or self.grau(y) == 0:
            return False

        lista_de_verticies_que_meu_x_esta_ligado = self.caminho_dois_vertices_aux(x, analizados)
        for i in range(len(lista_de_verticies_que_meu_x_esta_ligado)):
            if self.caminho_dois_vertices(lista_de_verticies_que_meu_x_esta_ligado[i], y, analizados):
                return True
        return False

    def caminho_dois_vertices_aux(self, x, analizados):
        L = []
        vertices = self.N
        arestas = self.A.values()

        for i in vertices:
            if i != x and i not in analizados:
                a = x + self.SEPARADOR_ARESTA + i
                if (a in arestas or a[::-1] in arestas):
                    L.append(i)
        return L


    def algoritmo_de_KRUSKAL(self):

        print("Algoritimo de KRUSKAL")

        verticesOriginais = self.N
        arestasOriginais = self.A


        lista_de_pesos_das_arestas_ordenadas = sorted(self.A.values())
        lista_arestar_ordenadas = []
        dic_resultado_final = {}


        # print(lista_de_pesos_das_arestas_ordenadas)
        while len(lista_de_pesos_das_arestas_ordenadas) > 0:
            for a in arestasOriginais:

                if len(lista_de_pesos_das_arestas_ordenadas) == 0:
                    break
                if arestasOriginais[a] == min(lista_de_pesos_das_arestas_ordenadas):
                        lista_arestar_ordenadas.append(a)
                        lista_de_pesos_das_arestas_ordenadas.remove(min(lista_de_pesos_das_arestas_ordenadas))

        # print(lista_de_pesos_das_arestas_ordenadas)
        # print(lista_arestar_ordenadas)



        lista_arestas_desconoexas = []
        lista_vertices_resultado_final = []
        lista_de_verticies_desconexos = []
        cont = 0

        for a in lista_arestar_ordenadas:
            v1, v2 = a.split(self.SEPARADOR_ARESTA)

            if cont == 0:
                dic_resultado_final[a] = arestasOriginais[a]
                lista_vertices_resultado_final.append(v1)
                lista_vertices_resultado_final.append(v2)
                cont+=1



            if (v1 in lista_vertices_resultado_final and v2 not in lista_vertices_resultado_final) or (v2 in lista_vertices_resultado_final and v1 not in lista_vertices_resultado_final):
                dic_resultado_final[a] = arestasOriginais[a]

                if v1 in lista_vertices_resultado_final:
                    lista_vertices_resultado_final.append(v2)
                    if v2 in lista_de_verticies_desconexos:
                        lista_de_verticies_desconexos.remove(v2)



                        for i in lista_arestas_desconoexas:
                            a, b = i.split(self.SEPARADOR_ARESTA)

                            if a == v2:
                                if b in lista_de_verticies_desconexos :
                                    lista_vertices_resultado_final.append(b)
                                    lista_de_verticies_desconexos.remove(b)
                            elif b == v2:
                                if a in lista_de_verticies_desconexos :
                                    lista_vertices_resultado_final.append(a)
                                    lista_de_verticies_desconexos.remove(a)


                else:
                    lista_vertices_resultado_final.append(v1)
                    if v2 in lista_de_verticies_desconexos:
                        lista_de_verticies_desconexos.remove(v1)

                        for i in lista_arestas_desconoexas:
                            a, b = i.split(self.SEPARADOR_ARESTA)

                            if a == v1:
                                if b in lista_de_verticies_desconexos and i in lista_vertices_resultado_final:
                                    lista_de_verticies_desconexos.remove(b)
                            elif b == v2:
                                if a in lista_de_verticies_desconexos and i in lista_vertices_resultado_final:
                                    lista_de_verticies_desconexos.remove(a)







            elif v1 in lista_de_verticies_desconexos or v2  in lista_de_verticies_desconexos:
                dic_resultado_final[a] = arestasOriginais[a]

                if v1 in lista_de_verticies_desconexos:
                    lista_de_verticies_desconexos.append(v2)
                else:
                     lista_de_verticies_desconexos.append(v1)
                lista_arestas_desconoexas.append(a)

            elif v1 not in lista_vertices_resultado_final and v2 not in lista_vertices_resultado_final:
                dic_resultado_final[a] = arestasOriginais[a]
                lista_arestas_desconoexas.append(a)
                lista_de_verticies_desconexos.append(v2)
                lista_de_verticies_desconexos.append(v1)






            # if v1 not in lista_verticies_passados and v2 not in lista_verticies_passados:
            #     lista_verticies_passados.append(v1)
            #     lista_verticies_passados.append(v2)
            #     dic_resultado_final[a] = arestasOriginais[a]
            #
            # elif v1 not in lista_verticies_passados and v2 in lista_verticies_passados:
            #     lista_verticies_passados.append(v1)
            #     dic_resultado_final[a] = arestasOriginais[a]
            # elif v2 not in lista_verticies_passados and v1 in lista_verticies_passados:
            #     lista_verticies_passados.append(v2)
            #     dic_resultado_final[a] = arestasOriginais[a]
            # dic_resultado_final[a] = arestasOriginais[a]
            if len(verticesOriginais) == len(lista_vertices_resultado_final):
                break



        print(dic_resultado_final)



    def algoritimo_de_PRIM(self):

        print("Algoritimo de PRIM")
        verticesOriginais = self.N
        arestasOriginais = self.A

        verticesVerificados = []
        arestasSelecionadas = {}

        # print(verticesOriginais)
        # print(arestasOriginais)

        maiorValor = 1000
        menorAresta = None
        proximoVertice = ''

        entrei = False

        while len(verticesVerificados) != len(verticesOriginais)-1:

            for a in arestasOriginais:
                v1, v2 = a.split(self.SEPARADOR_ARESTA)
                if (proximoVertice == v1 or proximoVertice == v2) and (a not in arestasSelecionadas.keys()) and (maiorValor > arestasOriginais[a]):

                    if (v1 == proximoVertice and v2 not in verticesVerificados) or (v2 == proximoVertice and v1 not in verticesVerificados):
                        maiorValor = arestasOriginais[a]
                        menorAresta = a
                        entrei = True



            if not entrei:
                maiorValor = 1000
                menorAresta = None

                for a in arestasOriginais:
                    v1, v2 = a.split(self.SEPARADOR_ARESTA)
                    if (maiorValor > arestasOriginais[a]) and (v1 not in verticesVerificados or v2 not in verticesVerificados) and (a not in arestasSelecionadas.keys()):

                        maiorValor = arestasOriginais[a]
                        menorAresta = a


            # print(maiorValor)
            # print(menorAresta)
            v1, v2 = menorAresta.split(self.SEPARADOR_ARESTA)
            if len(verticesVerificados) == 0:
                proximoVertice = v1
            if v1 not in verticesVerificados or v2 not in verticesVerificados:


                if v1 not in verticesVerificados and (v1 == proximoVertice ):
                    verticieDaVez = v1
                    proximoVertice = v2
                else:
                    verticieDaVez = v2
                    proximoVertice = v1

                verticesVerificados.append(verticieDaVez)
                arestasSelecionadas[menorAresta] = arestasOriginais[menorAresta]
                arestasOriginais.pop(menorAresta)



            entrei = False

            # print(verticesVerificados)

            # print(len(verticesVerificados))

        print(str(arestasSelecionadas))




    def __str__(self):
        '''
        Fornece uma representação do tipo String do grafo.
        O String contém um sequência dos vértices separados por vírgula, seguido de uma sequência das arestas no formato padrão.
        :return: Uma string que representa o grafo
        '''
        grafo_str = ''

        for v in range(len(self.N)):
            grafo_str += self.N[v]
            if v < (len(self.N) - 1):  # Só coloca a vírgula se não for o último vértice
                grafo_str += ", "

        grafo_str += '\n'

        for i, a in enumerate(self.A):
            grafo_str += self.A[a]
            if not (i == len(self.A) - 1):  # Só coloca a vírgula se não for a última aresta
                grafo_str += ", "

        return grafo_str
