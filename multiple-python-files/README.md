# Multi-File Apps

Multi-file apps actually work natively in SiS, though it is not possible today to
see or edit anything but the main file.

## Steps to make this work

1. Create your multi-file app and test it locally

   In this case, `streamlit run streamlit_app.py` should run the function imported from file2.py

2. Create the streamlit in SiS either through the snowcli or through the browser

   Through the snowcli, you can do

   ```sh
   snow streamlit create --file streamlit_app.py GREAT_NAME_FOR_MY_STREAMLIT
   snow streamlit deploy --file streamlit_app.py GREAT_NAME_FOR_MY_STREAMLIT
   ```

3. Upload the extra python file to the stage that was created for your streamlit

   ```sh
   snow stage put file2.py GREAT_NAME_FOR_MY_STREAMLIT_STAGE
   ```

4. Profit!
