import flaskr.index

if __name__=="__main__":
    flaskr.index.app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
