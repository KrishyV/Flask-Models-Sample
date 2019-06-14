@app.route('/autocomplete-colour', methods=['GET', 'POST'])
def autocomplete_singleColour():
    search = request.args.get('q') # This is from our autofill.js
    
    query = db.session.query(Color.color_design).filter(
        func.lower(Color.color_design).like('%' + str(search).lower().strip() + '%')))
        # This queries for similar entries in the dB
        
    results = [mv[0] for mv in query.all()]
    session.close()
    return jsonify(matching_results=results)
