class MessagesController < ApplicationController
    
    def index
        @messages = Message.all
    end
        
    def show 
        @message = Message.find(params[:id])
    end
    
    def new
        @message = Message.new
    end
    
    def create
        timestamp = Time.now.utc.iso8601
        @message = Message.new(message_params)
        
        if @message.save
            redirect_to @message
        else
            render 'new'
        end
    end
    
    private
        def message_params
            params.require(:message).permit(:title, :text)
        end
end
