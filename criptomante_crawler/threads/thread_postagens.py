from threading import Thread
from typing import List
from criptomante.repository.postagensRepository import PostagensRepository
from time import sleep
from criptomante.util.thread_util import ThreadUtil
from criptomante.model.postagem import Postagem
from criptomante_crawler.threads.minha_thread import MinhaThread

class ThreadPostagens(MinhaThread):
    #Atributos estáticos
    name = "ThreadPostagens"
    

    #Atributos de instância
    url : str
    crawler: object
    post: Postagem

    @classmethod
    def getCrawler(cls, website)->"AbstracrCrawler":
        from criptomante_crawler.crawlers.crawler_reddit import CrawlerReddit
        return CrawlerReddit()
    
    def executar(self):
        
        mensagens = self.crawler.processar_postagem(self.url, self.post)
        repository = PostagensRepository()
        repository.insereMensagens(mensagens, self.url)
        repository.sinalizaPostagemProcessada(self.url)
        self.continuar=False
                                                
    def mensagem_erro(self, e):
        print("Erro ao ler MSG "+self.url)
        print(e)
    
    @classmethod
    def fabricar(cls, limite,offset=0):
        saida=list()
        from criptomante_crawler.crawlers.abstract_crawler import AbstractCrawler
        repository = PostagensRepository()
        postagens = repository.obtemPostagensNaoProcessadasComExecutor(limit=limite)
        if len(postagens)==0:
            ThreadPostagens.esperando_novos=False
        for postagem in postagens:
            crawler:AbstractCrawler = ThreadPostagens.getCrawler(postagem.website)
            t = ThreadPostagens(daemon=True)
            t.url = postagem.url
            t.crawler = crawler
            t.post = postagem            
            saida.append(t)
        return saida





    