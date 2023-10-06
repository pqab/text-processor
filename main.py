import os
import importlib
from dotenv import dotenv_values

# Load config
config = dotenv_values('input/input.env')


# load all processors from the processor module
def load_processor() -> dict:
    processor = {}
    files = os.listdir('processor')
    for file in files:
        if file.endswith('.py') and file != '__init__.py':
            module_name = file[:-3]
            print(f'Loading module {module_name}')
            # Import the module dynamically
            try:
                processor[module_name] = importlib.import_module(f'processor.{module_name}')
                print(f'Loaded {module_name} - {processor[module_name]}')
            except ImportError as e:
                print(f'Failed to import {module_name}: {e}')
    return processor


processor = load_processor()


# run processor
processorResult = dict()
for p in config.get('processors').split(','):
    print(f'Running processor {p}')
    processorResult = processor.get(p).run(processorResult)
