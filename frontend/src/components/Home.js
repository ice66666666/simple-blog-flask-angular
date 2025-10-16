import React from 'react';
import { usePosts } from '../hooks/usePosts';
import PostCard from './PostCard';
import LoadingSpinner from './LoadingSpinner';

const Home = () => {
  const { posts, loading, error } = usePosts();

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <LoadingSpinner />
        <span className="ml-2 text-gray-600">Cargando posts...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="alert alert-error max-w-md mx-auto">
          <h3 className="font-semibold mb-2">Error al cargar los posts</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Bienvenido al Blog Simple
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Descubre historias, ideas y experiencias compartidas por nuestra comunidad.
          Únete a nosotros y comparte tu propia voz.
        </p>
      </div>

      {posts.length === 0 ? (
        <div className="text-center py-12">
          <div className="max-w-md mx-auto">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">📝</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No hay posts aún
            </h3>
            <p className="text-gray-600 mb-4">
              Sé el primero en compartir una historia con nuestra comunidad.
            </p>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Home;
