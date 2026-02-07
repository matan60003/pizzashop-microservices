# משתמשים בשרת Nginx קטן ויעיל
FROM nginx:alpine

# מעתיקים את קובץ ה-index.html שלנו לתיקייה ש-Nginx מכיר
COPY index.html /usr/share/nginx/html/index.html

# חושפים את פורט 80 (הפורט הסטנדרטי של אתרי אינטרנט)
EXPOSE 80