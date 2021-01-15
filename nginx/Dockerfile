FROM nginx:1.19.6-alpine

# デフォルトのconfを消して、別の設定を追加
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d