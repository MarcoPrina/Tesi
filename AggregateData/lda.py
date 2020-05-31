from gensim import corpora
import gensim
import pyLDAvis.gensim


class LDA():

    def findTopic(self, tokens, nTopic=5):
        self.dictionary = corpora.Dictionary(tokens)
        self.corpus = [self.dictionary.doc2bow(text) for text in tokens]

        self.ldamodel = gensim.models.ldamodel.LdaModel(self.corpus, num_topics=nTopic, id2word=self.dictionary, passes=15)
        self.ldamodel.save('model5.gensim')
        topics = self.ldamodel.print_topics(num_words=4)
        for topic in topics:
            print(topic)

    def display(self):
        lda_display = pyLDAvis.gensim.prepare(self.ldamodel, self.corpus, self.dictionary, sort_topics=False)
        pyLDAvis.display(lda_display)