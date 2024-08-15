# SimpleNERTagger (in Spanish)

by: [Jesús Armenta-Segura](https://jesusasmx.github.io/) ([CIC-IPN](https://cic.ipn.mx), [IFE LL&DH](https://ifelldh.tec.mx/en/data-hub))


This is a python library who can perform named-entity recognition (NER) for spanish text. It uses the Huggingface pipeline and can leverage any model compatible with the transformers pipeline.

### Why using this library?

The Huggingface pipeline already offers a few-lines solution for deploying a NER-tagger. This library also offers the follow features:

1.- Masks text with the tags obtained by the Huggingface method so it saves to you the tedious part of coding a masker. 
2.- Returns the tags in a well-ordered DataFrame format.
3.- It also includes two tag types not supported by the standard NER-taggers of Huggingface: telephone numbers and email addresses.


## Usage

```
!pip install SimpleNERtagger-ES
```

For now, only pip is supported for the installation. You can still fork this repo if needed.

## NER-tagging a text

First, import the tagger from the library:

```
from SimpleNERtagger_ES import NER_tagger
```

Second, call the method with a path to an existing model from Huggingface. In this example, the [spanish BETO + NER](https://huggingface.co/mrm8488/bert-spanish-cased-finetuned-ner) is used

```
## You may declare a Huggingface transformer finetunned for NER.
transformer = "mrm8488/bert-spanish-cased-finetuned-ner"

tags = NER_tagger(transformer)
```

Third, to perform the NER tagging over a text (in this case, a dummy text), it is necessary to define the tags. Currently (v0.2), this library supports four kinds of tags: emails, telephone numbers, names and locations.

Finally, the method who performs the NER tagging is named "NERtagging", its usage is straightforward and requires the follow arguments:

- ```texto```  The text to be tagged.
* ```enmascarar``` Means "to mask" in english. Set it False for not receiving a masked version of the text.
+ ```mails_tag``` The tag fot the email. Set it False for ignoring emails during the tagging.
+ ```tels_tag``` The tag fot the telephone numbers. Set it False for ignoring tel numbers during the tagging.
+ ```nombres_tag``` The tag fot the names. Set it False for ignoring names during the tagging.
+ ```lugares_tag``` The tag fot the places. Set it False for ignoring places during the tagging.

Here is the example of how to use it:

```

dummy_text = """Hola Joaquín, mi nombre es Máximo Décimo Meridio, vivo en Esmirna y soy un gladiador. 
Puedes.encontrarme.en  MDEcimoMeridio @ Colisseum-Romanorum-sanguinius.com.rome o bien en +56 23 4523 2453. 
También le puedes dejar un mensaje a mi patrón, en el correo Comodo.Joffrey@Colisseum-Romanorum.Exec.Boss.com.rome"""

masked_text, all_tags = tags.NERtagging(
    texto=dummy_text,
    enmascarar=True,            # Set it False for not receiving a masked version of the text.
    mails_tag="[MAIL]",         # Tag for emails.
    tels_tag="[TEL]",           # Tag for telephones.
    nombres_tag="[NOMBRE]",     # Tag for names.
    lugares_tag="[LUGAR]"       # Tag for places.
    )

print(masked_text)
print(all_tags)
```

This returns the string ```masked_text``` with the tagged text, and the pandas dataframe ```all_tags``` with all the tagged words (columns are "tag", "palabra" -word in spanish-, "start" and "end"). In this case:

```
Hola [NOMBRE], mi nombre es [NOMBRE] [NOMBRE] [NOMBRE], vivo en [LUGAR] y soy un gladiador. 
Puedes.encontrarme.en  [MAIL] o bien en[TEL]. 
También le puedes dejar un mensaje a mi patrón, en el correo [MAIL]

  tag        palabra	                                              start	end
0	[NOMBRE]  Joaquín	                                          5	12
1	[NOMBRE]	Máximo	                                          27	33
2	[NOMBRE]	Décimo	                                          34	40
3	[NOMBRE]	Meridio	                                          41	48
4	[LUGAR]	  Esmirna	                                          58	65
5	[MAIL]	  MDEcimoMeridio @ Colisseum-Romanorum-sanguiniu...      110	166
6	[TEL]	    +56 23 4523 2453	                                  176	193
7	[MAIL]	  Comodo.Joffrey@Colisseum-Romanorum.Exec.Boss.c...      257	310
```

As a toy example, consider this full snipet who unifies all the previous explanation:

```
from SimpleNERtagger_ES import NER_tagger

## You may declare a Huggingface transformer finetunned for NER.
transformer = "mrm8488/bert-spanish-cased-finetuned-ner"

## Custom tags:
custom_tag = ["[MAIL]",
              "[TEL]",
              "[NOMBRE]",
              "[LUGAR]"]

## Actual usage of the library.

tags = NER_tagger(transformer)

dummy_text = """Hola Joaquín, mi nombre es Máximo Décimo Meridio, vivo en Esmirna y soy un gladiador. 
Puedes.encontrarme.en  MDEcimoMeridio @ Colisseum-Romanorum-sanguinius.com.rome o bien en +56 23 4523 2453. 
También le puedes dejar un mensaje a mi patrón, en el correo Comodo.Joffrey@Colisseum-Romanorum.Exec.Boss.com.rome"""

masked_text, all_tags = tags.NERtagging(
    texto=dummy_text,
    enmascarar=True,            # Set it False for not receiving a masked version of the text.
    mails_tag=custom_tag[0],    # Tag for emails.
    tels_tag=custom_tag[1],     # Tag for telephones.
    nombres_tag=custom_tag[2],  # Tag for names.
    lugares_tag=custom_tag[3]   # Tag for places.
    )


print(f"\n\nThis is the original text:\n{dummy_text}\n\nThis is the masked text:\n{masked_text}\n")
try: # Displaying the dataframe may not work when running this code outside a jupyter notebook-like enviroment.
  print("Here is the dataset with the tags:\n")
  display(all_tags)
except:
  print(f"Here is the dataset with the tags:\n {all_tags}")
```

# Citation:

By using this work, you are also using the Huggingface transformer pipeline hence you are supedited to its licence. 
If using it on a paper, you shall cite both the employed Huggingface model and this repo.

# Release notes: 

Releases notes only documented for versions 0.2+
