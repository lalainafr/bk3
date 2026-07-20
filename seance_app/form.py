from django import forms
from .models import Cinema, Salle, Film, Evenement, Seance


# Cinema


class CreateCinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = "__all__"


class UpdateCinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = "__all__"


# Salle


class CreateSalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ["cinema", "numero", "capacite", "disponible"]

        widgets = {
            "cinema": forms.Select(attrs={"class": "form-control"}),
            "numero": forms.NumberInput(attrs={"class": "form-control"}),
            "capacite": forms.NumberInput(attrs={"class": "form-control"}),
            "disponible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class UpdateSalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ["cinema", "numero", "capacite", "disponible"]

        widgets = {
            "cinema": forms.Select(attrs={"class": "form-control"}),
            "numero": forms.NumberInput(attrs={"class": "form-control"}),
            "capacite": forms.NumberInput(attrs={"class": "form-control"}),
            "disponible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


# Film


class CreateFilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = [
            "titre",
            "duree",
            "genre",
            "date_sortie",
            "realisateur",
            "description",
            "affiche",
        ]

        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "duree": forms.NumberInput(attrs={"class": "form-control"}),
            "genre": forms.TextInput(attrs={"class": "form-control"}),
            "date_sortie": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "realisateur": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description du cinéma",
                    "rows": 5,
                    "cols": 40,
                }
            ),
            "affiche": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class UpdateFilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = [
            "titre",
            "duree",
            "genre",
            "date_sortie",
            "realisateur",
            "description",
            "affiche",
        ]

        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "duree": forms.NumberInput(attrs={"class": "form-control"}),
            "genre": forms.TextInput(attrs={"class": "form-control"}),
            "date_sortie": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "realisateur": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description du cinéma",
                    "rows": 5,
                    "cols": 40,
                }
            ),
            "affiche": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


# Evenement


class CreateEvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ["titre", "genre", "description", "affiche"]

        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "genre": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description du évenement",
                    "rows": 5,
                    "cols": 40,
                }
            ),
            "affiche": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class UpdateEvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ["titre", "genre", "description", "affiche"]

        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "genre": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description du évenement",
                    "rows": 5,
                    "cols": 40,
                }
            ),
            "affiche": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


# Seance


class CreateSeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ["film", "evenement", "salle", "date", "horaire"]

        widgets = {
            "film": forms.Select(attrs={"class": "form-control"}),
            "evenement": forms.Select(attrs={"class": "form-control"}),
            "salle": forms.Select(attrs={"class": "form-control"}),
            "horaire": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class UpdateSeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = [
            "film",
            "evenement",
            "salle",
            "date",
            "horaire",
        ]

        widgets = {
            "film": forms.Select(attrs={"class": "form-control"}),
            "evenement": forms.Select(attrs={"class": "form-control"}),
            "salle": forms.Select(attrs={"class": "form-control"}),
            "horaire": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
