# Redis Start

<pre><code>docker run --name redis -p 6379:6379 --network redis-net -d redis redis-server --appendonly yes</code></pre>


<hr>

# Celery Start

<pre><code>celery -A backend worker -l info --concurrency=1 -P gevent</code></pre>