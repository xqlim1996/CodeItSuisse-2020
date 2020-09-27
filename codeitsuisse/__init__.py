from flask import Flask;
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.contact_tracing
import codeitsuisse.routes.inventory_management
import codeitsuisse.routes.pretick
import codeitsuisse.routes.supermarket



