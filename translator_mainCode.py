import customtkinter as ctk
from deep_translator import GoogleTranslator
import arabic_reshaper as ar  #to reshape the arabic translation
from bidi.algorithm import get_display 
ctk.set_appearance_mode ("dark")
ctk.set_default_color_theme ("green")
app=ctk.CTk()
app.title("Translation Model By(Samy Elrefaey)")
app.geometry("1280x1019")
langs_mapping = {               #the languages that we will provide in this code 
    "Arabic": "ar",
    "French": "fr",
    "English": "en",
    "German": "de",
    "Spanish": "es"
}
langs=list(langs_mapping.keys())
from_lang=ctk.CTkComboBox(app,values=langs)
from_lang.set("English")   # the default
from_lang.place(x=415,y=155)
to_lang =ctk.CTkComboBox(app,values=langs)
to_lang.set("Arabic")
to_lang.place(x=1300,y=155)
label = ctk.CTkLabel(app,text=" Enter the text ",font=("Times New Roman",30))     #labels 
label.place(x=200,y=150)
label2 = ctk.CTkLabel(app,text="Translation",font=("Times New Roman",30))   
label2.place(x=1100,y=150)
input_box=ctk.CTkTextbox(app,width=600,height=400,font=("Arial",30))    #txt box to input the txt
input_box.place(x=55,y=300)
output_box=ctk.CTkTextbox(app,width=600,height=400,font=("Arial",30))   #txt box 2  the translation box
output_box.place(x=850,y=300)
labelArrow=ctk.CTkLabel(app,text="➬",font=("Arial",70))        #arrow 
labelArrow.place(x=720,y=400)
def translate():
    text=input_box.get("1.0","end")             # to get the text that well be translated 
    source = langs_mapping[from_lang.get()]
    target = langs_mapping[to_lang.get()]
    translated_txt=GoogleTranslator(source=source,target=target).translate(text)
    if target=="ar":
       reshaped_txt=ar.reshape(translated_txt)
       translated_txt=bidi_txt= get_display(reshaped_txt)
    output_box.delete("1.0","end")
    output_box.insert("1.0",translated_txt)
def copy():              #function to copy the translated_txt
    text=output_box.get("1.0","end")
    reshaped_txt=ar.reshape(text)
    text=bidi_txt= get_display(reshaped_txt)
    app.clipboard_clear()
    app.clipboard_append(text)
    app.update()
copy_button=ctk.CTkButton(app,text="copy",font=("Arial",30),command=copy)
copy_button.place(x=1200,y=730)
button=ctk.CTkButton(app,text="translate",font=("Arial",20),command=translate)
button.place(x=680,y=500)
app.mainloop()
