# SimpleNERTagger (in Spanish)

by: Jesús Armenta-Segura (CIC-IPN, IFE DH&LL)

This is a library who can perform named-entity recognition (NER) for spanish text. It uses the Huggingface pipeline and can leverage any model compatible with the transformers pipeline.

### Why using this library?

The Huggingface pipeline already offers a few-lines solution for deploying a NER-tagger. This library also offers the follow features:

1.- Masks text with the tags obtained by the Huggingface method so it saves to you the tedious part of coding a masker. 
2.- Returns the tags in a well-ordered DataFrame format.
3.- It also includes two tag types not supported by the standard NER-taggers of Huggingface: telephone numbers and email addresses.


## Usage



