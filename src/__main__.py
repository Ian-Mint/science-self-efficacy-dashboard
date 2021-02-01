from .ui import app
# noinspection PyUnresolvedReferences
import src.ui.dashboard
import os

app.run_server(debug=False,
               dev_tools_hot_reload=False,
               host=os.getenv("HOST", "localhost"),
               port=os.getenv("PORT", "8050"),
               )
