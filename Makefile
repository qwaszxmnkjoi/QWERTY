check_sure:
	@( read -p "Are you sure? [y/N]: " sure && case "$$sure" in [yY]) true;; *) false;; esac )

run-update: check_sure
	@echo "STEP 0. Pull"
	@git pull origin main
	@echo "STEP 1. Run Containers"
	@docker-compose up -d --build
	@echo "STEP 2. Apply migrations:"
	@docker exec -it emigrant-python-1 python manage.py migrate
	@echo "STEP 3. Collect static:"
	@cp -r app/static/* var/static
	@docker exec -it emigrant-python-1 python manage.py collectstatic --no-input
	@echo "STEP 4. Compile translations: "
	@docker exec -it emigrant-python-1 python manage.py create_messages --only-new
	@echo "STEP 5. Restart: "
	@docker restart emigrant-python-1
