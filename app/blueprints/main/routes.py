from flask import render_template, flash
import requests
from .forms import SearchForm
from flask_login import login_required
from .import bp as main

@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/pokemon', methods=['GET','POST'])
@login_required
def pokemon():
    pokemon_name = None
    form = SearchForm()
    # Validate Form
    if form.validate_on_submit():
        pokemon_name = form.pokemon_name.data.lower()
        form.pokemon_name.data = '' #clear form after hitting search
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        if response.ok:
            data = response.json()
            if not data:
                flash("Something went wrong. Couldn't connect the library.",'danger')
                return render_template("pokemon.html.j2", form=form)
            
            pokemon_dict = {
                'pokemon_image': data['sprites']['other']['dream_world']['front_default'],
                'pokemon_name': data['name'],
                'ability_name': data['abilities'][0]['ability']['name'],
                'base_experience': data['base_experience'],
                'sprite_ULR': data['sprites']['front_shiny']
                }
            return render_template("pokemon.html.j2", form=form, pokemon = pokemon_dict)
        flash(f'There is no pokemon named {pokemon_name}','warning')
        return render_template("pokemon.html.j2", form=form)
    return render_template('pokemon.html.j2', form=form)
    