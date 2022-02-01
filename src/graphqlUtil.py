import graphene
import logging

class getQuery(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value='World'))

    def resolve_hello(self, info, name):
        return 'Hello ' + name


if __name__ == '__main__':
    try:
        logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)
        schema = graphene.Schema(query=getQuery)
        result = schema.execute('{ hello }')
        logging.info(result.data['hello'])
    except Exception as err:
        logging.error(err)
        exit(-1)

    logging.info('completed.')
    exit(0)