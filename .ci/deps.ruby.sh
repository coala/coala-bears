# Remove Ruby directive from Gemfile as we test many versions
sed -i.bak '/^ruby/d' Gemfile

if [ "$TRAVIS_RUBY_VERSION" != "2.1" ]; then
  gem update --system
fi

# Install maximum version of bundler for each Ruby version
if [ "$TRAVIS_RUBY_VERSION" = "2.1" ]; then
  gem install bundler -v 1.16.1
elif [ "$TRAVIS_RUBY_VERSION" = "2.2" ]; then
  gem install bundler -v 1.17.3
else
  gem install bundler
fi
