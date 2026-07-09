#!bin/bash

# A persistent volume mounted at frappe-bench is created by Docker (root-owned)
# before this script runs. It's an active mount point, so it can't be removed
# to let `bench init` create it fresh, and it isn't writable by the frappe
# user until reowned.
sudo chown frappe:frappe /home/frappe/frappe-bench 2>/dev/null

if [ -d "/home/frappe/frappe-bench/apps/frappe" ]; then
    echo "Bench already exists, skipping init"
    cd frappe-bench
    bench start
else
    echo "Creating new bench..."
fi

export PATH="${NVM_DIR}/versions/node/v${NODE_VERSION_DEVELOP}/bin/:${PATH}"

if [ ! -d "/home/frappe/frappe-bench/apps/frappe" ]; then
    # Can't init directly into the mounted (existing) frappe-bench directory,
    # so init into a scratch dir and move the result into the mount point.
    bench init --skip-redis-config-generation frappe-bench-tmp
    shopt -s dotglob
    mv frappe-bench-tmp/* /home/frappe/frappe-bench/
    shopt -u dotglob
    rmdir frappe-bench-tmp
    # The venv's editable install of frappe still points at the old
    # frappe-bench-tmp path post-move ("No module named 'frappe'").
    # Reinstall it in place now that it lives at its final path.
    /home/frappe/frappe-bench/env/bin/python -m pip install --quiet --force-reinstall --no-deps -e /home/frappe/frappe-bench/apps/frappe
fi

cd frappe-bench

# Use containers instead of localhost
bench set-mariadb-host mariadb
bench set-redis-cache-host redis://redis:6379
bench set-redis-queue-host redis://redis:6379
bench set-redis-socketio-host redis://redis:6379

# Remove redis, watch from Procfile
sed -i '/redis/d' ./Procfile
sed -i '/watch/d' ./Procfile

bench get-app payments
bench get-app lms https://github.com/Ouchandid/lms.git --branch develop

bench new-site lms.localhost \
--force \
--mariadb-root-password 123 \
--admin-password admin \
--no-mariadb-socket

bench --site lms.localhost install-app payments
bench --site lms.localhost install-app lms
bench --site lms.localhost set-config developer_mode 1
bench --site lms.localhost clear-cache
bench use lms.localhost

bench start
