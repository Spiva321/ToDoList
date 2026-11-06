/**
 * Прогрессивное улучшение интерфейса.
 * Базовая работа приложения (добавление, удаление, переключение статуса)
 * полностью доступна и без JavaScript.
 */
document.addEventListener('DOMContentLoaded', () => {
    const toggles = document.querySelectorAll('.task__toggle');

    toggles.forEach((form) => {
        const checkbox = form.querySelector('.task__checkbox');
        if (!checkbox) {
            return;
        }

        checkbox.addEventListener('change', () => {
            form.classList.add('is-busy');
            form.submit();
        });
    });

    document.querySelectorAll('.task__delete').forEach((form) => {
        form.addEventListener('submit', (event) => {
            const confirmed = window.confirm('Удалить эту задачу?');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // Плавное появление карточек при загрузке страницы.
    const list = document.querySelector('.task-list');
    if (list) {
        list.classList.add('is-animated');
    }
});
