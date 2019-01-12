# *sign_compare*
A simple tool to compare (linguistic) signs.

*sign_compare* provides a simple tool to compare signs (especially in a linguistic sense) by calculating both the [Dice coefficient](https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient) and the [Jaccard index](https://en.wikipedia.org/wiki/Jaccard_index). For both measurements are working on sets and compare elements of two sets with each other, *sign_compare* also comes with a tool to create new signs and to add or remove features. This allows researchers to enter their results of, for example, a corpus analysis to calculate similarities between two signs. Those signs can be certain words or morphemes but even a so-called "[wortverbund](http://www.baer-linguistik.de/hlr/028.htm)". Through this, *sign_compare* lends itself to compare literary characters with each other taking into account all the semantic features that determine them within the story.

*sign_compare* is based on GUIs so you can easily provide it to researchers who aren’t used to work with Python codes (you could, for example, create an executable file for them).

## Remarks on how to use *sign_compare*
*sign_compare* is a simple, self-explanatory tool. The only thing that requires further explanation might be the fact that it is possible to add all the features of an already created sign at once to another already created sign. If, for example, a sign "woman" contains the features "person", "female" and "adult" you can add them all together to a sign like "queen" by entering "woman.sign" in the entry at "Add feature(s)".  
Notice that you should always enter the same feature in the same way in order to get helpful results (e.g. stick to a feature "human" instead of varying by using different labels like "human", "homo sapiens" or "person"). Some exemplary signs (representing German words) can be found in this package as well (see "[sc_files](sc_files)").

## License
The work contained in this package is licensed under the Apache License, Version 2.0 (see the file "[LICENSE](LICENSE.txt)").
