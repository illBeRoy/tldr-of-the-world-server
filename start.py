import server
import context
import endpoints
import middlewares.cors


if __name__ == '__main__':
    app = server.Server(__name__)

    app.set_context('proximity_graph', context.proximity_graph)
    app.set_context('names', context.names)
    app.set_context('group_enrich', context.group_enrich)
    app.set_context('feed', context.feed)
    app.set_context('biography', context.biography)

    app.use_middleware(middlewares.cors.middleware)

    app.use(endpoints.all)
    app.run(3001)
