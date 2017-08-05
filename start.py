import server
import endpoints.people.suggestions


if __name__ == '__main__':
    app = server.Server(__name__)
    app.use(endpoints.people.suggestions.Endpoint)
    app.run(3000)
