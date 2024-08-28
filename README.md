# SimpleNERTagger (for Spanish)

by: [Jesús Armenta-Segura](https://jesusasmx.github.io/) ([CIC-IPN](https://cic.ipn.mx), [IFE LL&DH](https://ifelldh.tec.mx/en/data-hub))


This is a python library who can perform named-entity recognition (NER) for spanish text. It uses the Huggingface pipeline and can leverage any model compatible with the transformers pipeline.

### Why using this library?

The Huggingface pipeline already offers several few-lines solutions for deploying a NER-tagger. This library also offers the follow features:

1. Masks text with the tags obtained by the Huggingface method. Hence, it saves to you the tedious part of coding a masker. 
2. Returns the tags in a well-ordered DataFrame format.
3. It also includes two **tag types** not supported by the standard Huggingface NER-taggers: telephone numbers and email addresses.


## Usage

```
>>> !pip install SimpleNERtagger-ES
```

For updating into a the latest version, use this instead:
```
>>> !pip install SimpleNERtagger-ES --upgrade
```

For now, only pip is supported for the installation. You can still fork this repo if needed.

## NER-tagging a text

First, import the tagger from the library:

```
>>> from SimpleNERtagger_ES import NER_tagger
```

Second, call an instance of the **NER_tagger** class with a path to an existing model from Huggingface. In this example, the [spanish BETO + NER](https://huggingface.co/mrm8488/bert-spanish-cased-finetuned-ner) is used. In general, you may declare a Huggingface transformer finetunned for NER.

```
>>> transformer = "mrm8488/bert-spanish-cased-finetuned-ner"
>>> tags = NER_tagger(transformer)
```

**IMPORTANT:** If you declare a non-existing model, or it is not suitable for NER-tagging, or you just do not declare a model, the library will not load a transformer and hence will only can tag emails and telephones.
  

Third, to perform the NER tagging over a text (in this case, a dummy text), it is necessary to define the tags. Currently (v0.2+), this library supports four kinds of tags: emails, telephone numbers, names and locations and it is not sensitive to the BIO notation since it only considers complete words.

Finally, the method who performs the NER tagging is named "NERtagging", its usage is straightforward and it requires the follow arguments:

- ```texto```  The text to be tagged.
* ```unir_tags_iguales``` Means "join_equal_tags" in english. If True, all contiguous tags will be unified as one. For instance, "Juán Pérez" can represent two contiguous name tags if ```unir_tags_iguales=False```.
+ ```mails_tag``` The tag fot the email. Set it False for ignoring emails during the tagging.
+ ```tels_tag``` The tag fot the telephone numbers. Set it False for ignoring tel numbers during the tagging.
+ ```nombres_tag``` The tag fot the names. Set it False for ignoring names during the tagging.
+ ```lugares_tag``` The tag fot the places. Set it False for ignoring places during the tagging.

Here is the example of how to use it:

```
>>> dummy_text = """Hola Joaquín, mi nombre es Máximo Décimo Meridio, vivo en Esmirna y soy un gladiador. 
Puedes.encontrarme.en  MDEcimoMeridio @ Colisseum-Romanorum-sanguinius.com.rome o bien en +56 23 4523 2453. 
También le puedes dejar un mensaje a mi patrón, en el correo Comodo.Joffrey@Colisseum-Romanorum.Exec.Boss.com.rome, 
lo cual muestra que somos una gran familia."""

>>> masked_text, all_tags = tags.NERtagging(
      texto=dummy_text,
      unir_tags_iguales=True,     # Set it False for convert "Maximo Décimo Meridio" into [NOMBRE] [NOMBRE] [NOMBRE] rather than a single [NOMBRE].
      mails_tag="[MAIL]",         # Tag for emails. If False, avoids emails during the tagging.
      tels_tag="[TEL]",           # Tag for telephones. If False, avoids telepehones during the tagging.
      nombres_tag="[NOMBRE]",     # Tag for names. If False, avoids names during the tagging.
      lugares_tag="[LUGAR]"       # Tag for places. If False, avoids places during the tagging.
      )
```

```tags.NERtagging(*args)``` returns the string ```masked_text```, which is the input text but tagged, and the pandas dataframe ```all_tags```, which contains all the tagged words (columns are "tag", "palabra" -word in spanish-, "start" and "end") in an ordered fashion. In this case:

```
>>> print(masked_text)

Hola [NOMBRE], mi nombre es [NOMBRE], vivo en [LUGAR] y soy un gladiador. 
Puedes.encontrarme.en  [MAIL] o bien en[TEL]. 
También le puedes dejar un mensaje a mi patrón, en el correo [MAIL], 
lo cual muestra que somos una gran familia.
```
```
>>> print(all_tags)

        tag                                            palabra  start  end
0  [NOMBRE]                                            Joaquín      5   12
1  [NOMBRE]                              Máximo Décimo Meridio     27   48
2   [LUGAR]                                            Esmirna     58   65
3    [MAIL]  MDEcimoMeridio @ Colisseum-Romanorum-sanguiniu...    110  166
4     [TEL]                                   +56 23 4523 2453    176  193
5    [MAIL]  Comodo.Joffrey@Colisseum-Romanorum.Exec.Boss.c...    257  310
```

As a toy example, consider this full snipet.py who unifies all the previous procedure into a single script:

```
from SimpleNERtagger_ES import NER_tagger

## You may declare a Huggingface transformer finetunned for NER.
transformer = "mrm8488/bert-spanish-cased-finetuned-ner"

## Custom tags:
custom_tag = ["[MAIL]",
              "[TEL]",
              "[NOMBRE]",
              "[LUGAR]"]

## Actual usage of the library:

tags = NER_tagger(transformer)

dummy_text = """Hola Joaquín, mi nombre es Máximo Décimo Meridio, vivo en Esmirna y soy un gladiador. 
Puedes.encontrarme.en  MDEcimoMeridio @ Colisseum-Romanorum-sanguinius.com.rome o bien en +56 23 4523 2453. 
También le puedes dejar un mensaje a mi patrón, en el correo Comodo.Joffrey@Colisseum-Romanorum.Exec.Boss.com.rome, 
lo cual muestra que somos una gran familia."""

masked_text, all_tags = tags.NERtagging(
    texto=dummy_text,
    unir_tags_iguales=True,     # Set it False for convert "Maximo Décimo Meridio" into [NOMBRE] [NOMBRE] [NOMBRE] rather than a single [NOMBRE].
    mails_tag=custom_tag[0],    # Tag for emails.
    tels_tag=custom_tag[1],     # Tag for telephones.
    nombres_tag=custom_tag[2],  # Tag for names.
    lugares_tag=custom_tag[3]   # Tag for places.
    )


print(f"\n\nThis is the original text:\n{dummy_text}\n\nThis is the masked text:\n{masked_text}\n")
try: # Displaying the dataframe may not work when running this code outside a jpnb-like enviroment.
  print("Here is the dataset with the tags:\n")
  display(all_tags)
except:
  print(f"Here is the dataset with the tags:\n {all_tags}")
```

### BONUS: using this NER-tagger in a Pandas Dataframe

Perhaps you may want to use it for masking text over the rows of a DataFrame. On that case, the use is straightforward:

First, get your dataframe. As a toy example, consider this [HuggingFace dataset for spanish jokes](https://huggingface.co/datasets/mrm8488/CHISTES_spanish_jokes) (we take only the 100 first samples):
```
>>> import pandas as pd
>>> df = pd.read_parquet("hf://datasets/mrm8488/CHISTES_spanish_jokes/data/train-00000-of-00001-b70fa6139e8c3f32.parquet").head(100)
```

Second, initialize the methods (such as in the previous example):
```
>>> from SimpleNERtagger_ES import NER_tagger
>>> transformer = "mrm8488/bert-spanish-cased-finetuned-ner"
>>> tags = NER_tagger(transformer)
```

Third, run the tagger over all rows by using the ```lambda``` function and the ```progress_apply``` pandas' method. 
Recall that ```tags.NERtagging(**args)``` returns two values: the masked text and the dataframe with the tags. In order to store the masked texts into a new column, while setting apart the dataframes at the same time, we can use the ```zip(*)``` function to do so:
```
>>> from tqdm import tqdm # In some envoroments you should want to run "!pip install tqdm" first. 
>>> tqdm.pandas(desc="Añadiendo NER tags y enmascarando") #tqdm is only for showing a nice progress bar.
>>> df["NER_tagged_text"], its_tags = zip(*df["text"].progress_apply(lambda x: tags.NERtagging(texto=x, 
                                                                                           unir_tags_iguales=True, 
                                                                                           mails_tag="[MAIL]", 
                                                                                           tels_tag="[TEL]", 
                                                                                           nombres_tag="[NOMBRE]", 
                                                                                           lugares_tag="[LUGAR]")))
```
WARNING: Output might be ludicrously humongous.

Here is a full script who contains all the previous explanation:
```
## Suppose that you use a HuggingFace dataset:

import pandas as pd

#This is a datasets for spanish jokes. The texts are stored into a column named "text". We consider only the first 100 as an example.
df = pd.read_parquet("hf://datasets/mrm8488/CHISTES_spanish_jokes/data/train-00000-of-00001-b70fa6139e8c3f32.parquet").head(100)

## Method initialization:
from SimpleNERtagger_ES import NER_tagger

transformer = "mrm8488/bert-spanish-cased-finetuned-ner"
custom_tag = ["[MAIL]",
              "[TEL]",
              "[NOMBRE]",
              "[LUGAR]"]

tags = NER_tagger(transformer)


## How to use the method in that pandas dataframe:

from tqdm import tqdm # In some cases you might want to run "!pip install tqdm" first. tqdm is only for showing a nice progress bar.
tqdm.pandas(desc="Añadiendo NER tags y enmascarando")


## If you want to remove tqdm, just change ".progress_apply" to ".apply".
## Recall that NERtagging has two outputs: the masked text and a dataframe with the tags. The use of zip allow us to generate the
## new column with the masked texts, but also to store back into "its_tags" the dataframes with the tags, which are ordered
## like the rows (e.g. the kth element of "its_tags" corresponds to the tag dataframe for the kth row. It is not in terms of the index)
df["NER_tagged_text"], its_tags = zip(*df["text"].progress_apply(lambda x: tags.NERtagging(texto=x, 
                                                                                           unir_tags_iguales=True, 
                                                                                           mails_tag=custom_tag[0], 
                                                                                           tels_tag=custom_tag[1], 
                                                                                           nombres_tag=custom_tag[2], 
                                                                                           lugares_tag=custom_tag[3])))

#This is the column with the tagged texts:
try:
  display(df[["text", "NER_tagged_text"]])
except:
  print(df[["text", "NER_tagged_text"]])

#The diverse dataframes with the tags are stored in the variable "its_tags".
for count, all_tags in enumerate(its_tags): #WARNING: Output may be ludicrously humongous.
  try:
    print(f"\nRow {count}:")
    display(all_tags)
  except:
    print(f"\nRow {count}:")
    print(all_tags)
```


# Citation:

By using this work, you are also using the Huggingface transformer pipeline. Hence, you are supedited to its licence. 
If using this work for/on a paper, you must cite both the employed Huggingface model and this repo.

# Release notes and changelogs: 

_Releases notes only documented for versions 2+_

### Version 2.3

- Fixed the problem of not retrieving the text after the last tag.
- Argument "enmascarar" removed for being redundant (if you want an unmasked text, just do not overwrite the "texto" variable), and substituted by the argument "unir_tags_iguales".
- Function "tag_transformers" optimized.
- Method "NERtagging" optimized.
