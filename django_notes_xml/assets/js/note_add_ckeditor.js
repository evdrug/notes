window.onload = function () {
    const saveButton = document.querySelector('#save');
    let text_button = saveButton.innerHTML

    ClassicEditor
        .create(document.querySelector('#id_add_text_area'),
            {
                toolbar: ['bold', 'italic', '|', 'undo', 'redo', '|', 'bulletedList', 'numberedList', 'blockQuote'],
            }
        )
        .then(editor => {
            handleSaveButton(editor);
        })
        .catch(error => {
            console.error(error);
        });

    function clearEditor(editor) {
        saveButton.disabled = true
        saveButton.classList.remove('btn-seccuss')
        saveButton.classList.add('btn-disable')
        editor.setData('');
        editor.isReadOnly = false;
    }

    function addMessage(text, type = 'alert-info') {
        let wrapp_div = document.createElement("div");
        let close_button = document.createElement("button");
        close_button.innerHTML = '<span aria-hidden="true">×</span>'
        close_button.classList.add('close')

        wrapp_div.classList.add('alert')
        wrapp_div.classList.add(type)
        wrapp_div.innerHTML = `${text}`;
        wrapp_div.append(close_button)
        saveButton.after(wrapp_div);
        close_button.addEventListener('click', () => {
            wrapp_div.remove()
        })
    }

    function handleSaveButton(editor) {
        saveButton.addEventListener('click', evt => {
            const data = editor.getData();
            const headers = new Headers({
                'X-CSRFToken': token,
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
            });
            evt.preventDefault();
            editor.isReadOnly = true; //  блочим поле редактора, когда сохраняются данные
            saveButton.disabled = true
            saveButton.innerHTML = '<span class="spinner-circle spin"></span>'


            fetch(url, {
                body: JSON.stringify({note: data}),
                method: 'POST',
                headers: headers
            })
                .then(response => {
                    if (!response.ok) {
                        throw Error(`Ошибка ${response.status} : ${response.statusText}`);
                    }
                    return response.json()
                })
                .then(response => {
                    clearEditor(editor)
                    saveButton.innerHTML = text_button
                    addMessage(`Заметка добавлена! <a href="${response['link']}">${response['link']}</a>`, 'alert-success')
                })
                .catch(error => {
                    editor.isReadOnly = false;
                    saveButton.disabled = false
                    saveButton.innerHTML = text_button
                    addMessage(`${error.message}`, 'alert-danger')
                });

        });


        let ck_box = document.querySelector('div[role="textbox"]')

        // блочим кнопку сохранения, если пустое поле заметки
        if (ck_box.querySelector('p:first-child br[data-cke-filler=true]')) {
            saveButton.disabled = true
            saveButton.classList.remove('btn-seccuss')
            saveButton.classList.add('btn-disable')
        }

        // если чтото введено в поле заметки, разблокируем кнопку сохранения
        ck_box.addEventListener('keyup', () => {
            if (ck_box.querySelector('p:first-child br[data-cke-filler=true]')) {
                saveButton.disabled = true
                saveButton.classList.remove('btn-seccuss')
                saveButton.classList.add('btn-disable')
            } else {
                saveButton.disabled = false
                saveButton.classList.remove('>btn-disable')
                saveButton.classList.add('btn-seccuss')
            }
        })
    }
};