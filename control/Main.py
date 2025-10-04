from control.PipelineController import PipelineController

if __name__ == '__main__':
    controller = PipelineController(total_books=135)
    controller.pipeline(books_to_download=20)