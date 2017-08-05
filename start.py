import server
import context
import endpoints.people
import middlewares.cors


if __name__ == '__main__':
    app = server.Server(__name__)

    app.set_context('proximity_graph', context.proximity_graph)
    app.set_context('names', context.names)

    app.use_middleware(middlewares.cors.middleware)

    app.use(endpoints.people.all)
    app.run(3001)
