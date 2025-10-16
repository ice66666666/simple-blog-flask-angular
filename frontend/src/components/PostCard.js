import React from 'react';
import { Calendar, User } from 'lucide-react';
import { formatters } from '../utils';

const PostCard = ({ post }) => {
  return (
    <article className="card hover:shadow-lg transition-all duration-300">
      <div className="card-body">
        <h3 className="text-xl font-semibold text-gray-900 mb-3 line-clamp-2">
          {post.title}
        </h3>
        
        <p className="text-gray-600 mb-4 line-clamp-3">
          {formatters.truncateText(post.content, 150)}
        </p>
        
        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <User size={14} />
            <span className="font-medium">{post.author}</span>
          </div>
          
          <div className="flex items-center gap-1">
            <Calendar size={14} />
            <span>{formatters.formatDateShort(post.created_at)}</span>
          </div>
        </div>
      </div>
    </article>
  );
};

export default PostCard;
